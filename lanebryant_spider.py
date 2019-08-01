import json
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from lanebryant.items import LaneBryantItem


class LanebryantSpider(CrawlSpider):
    name = "lanebryant_spider"
    allowed_domains = ["lanebryant.com"]
    start_urls = ["http://www.lanebryant.com/"]

    currency = "CA"
    retailer = "lanebryant-ca"
    lang = "en"
    market = "CA"

    gender = "Women"

    restrict_home_css = ["#asc-header-con", ".mar-pagination-section"]
    restrict_product_css = [".inverted", ]

    rules = (
        Rule(LinkExtractor(restrict_css=restrict_home_css)),
        Rule(LinkExtractor(restrict_css=restrict_product_css), callback="parse_item"),
    )

    def parse_item(self, response):
        garment = LaneBryantItem()
        garment["name"] = self.get_product_name(response)
        garment["description"] = self.get_product_description(response)
        garment["retailer_sku"] = self.get_retailer_sku(response)
        garment["image_urls"] = self.get_image_urls(response)
        garment["care"] = self.get_product_care(response)
        garment["url"] = response.url
        garment["lang"] = self.lang
        garment["currency"] = self.currency
        garment["brand"] = self.get_product_brand(response)
        garment["category"] = self.get_product_category(response)
        garment["crawl_start_time"] = datetime.now().isoformat()
        garment["date"] = int(datetime.timestamp(datetime.now()))
        garment["crawl_id"] = self.get_crawl_id()
        garment["market"] = self.market
        garment["retailer"] = self.retailer
        garment["gender"] = self.gender
        garment["price"] = self.get_product_price(response)
        garment["skus"] = self.get_product_skus(response)

        yield garment

    def clean_price(self, price):
        return price.replace(".", "").replace("$", "")

    def clean(self, json_text):
        return json_text.replace("\n", "").replace("\\", "").replace("\r", "").replace("\'", "")

    def get_product_json(self, response):
        xpath = "//script[@type='application/ld+json']//text()"
        return json.loads(self.clean(response.xpath(xpath).get())[:-2])

    def get_sku_json(self, response):
        css = "#pdpInitialData::text"
        return json.loads(response.css(css).get())

    def get_product_name(self, response):
        return response.css(".mar-product-title::text").get()

    def get_product_description(self, response):
        return [self.get_product_json(response)["description"]]

    def get_retailer_sku(self, response):
        return self.get_product_json(response)["sku"]

    def get_image_urls(self, response):
        return [images["sku_image"].replace("//", "", 2) for images in
                self.get_sku_json(response)["pdpDetail"]["product"][0]["all_available_colors"][0]["values"]]

    def get_product_price(self, response):
        return self.clean_price(self.get_product_json(response)["offers"]["price"])

    def get_product_care(self, response):
        css = ".mar-product-additional-info #tab1 li:not(:first-child)::text"
        return [care.strip() for care in response.css(css).getall()]

    def get_product_brand(self, response):
        return response.css("a.lb> h2::text").get()

    def get_product_category(self, response):
        xpath = "//script[@type='text/javascript']//text()"
        category = response.xpath(xpath).re_first('pageName": "(.+?)"')
        return category.replace(" ", "").split(":")

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d-%H%M%s')}-medp"

    def get_product_sizes(self, response):
        return {sizes["id"]: sizes["value"] for sizes in
                self.get_sku_json(response)["pdpDetail"]["product"][0]["all_available_sizes"][0]["values"]}

    def get_product_colors(self, response):
        return {colors["id"]: colors["name"] for colors in
                self.get_sku_json(response)["pdpDetail"]["product"][0]["all_available_colors"][0]["values"]} or {}

    def get_previous_price(self, parsed_json):
        if parsed_json['list_price'] is not parsed_json["sale_price"]:
            return {'previous_price': self.clean_price(parsed_json['list_price'])}

    def get_product_skus(self, response):
        skus = {}

        parsed_json = self.get_sku_json(response)
        sizes = self.get_product_sizes(response)
        colors = self.get_product_colors(response)
        common_sku = self.get_previous_price(parsed_json["pdpDetail"]["product"][0]["skus"][0]["prices"]) or {}

        for item in parsed_json["pdpDetail"]["product"][0]["skus"]:
            sku = common_sku.copy()
            sku["price"] = self.clean_price(item["prices"]["sale_price"])
            sku["color"] = colors[item["color"]]
            sku["size"] = sizes[item["size"]] if item["size"] in sizes else item["size"]
            if not parsed_json["pdpDetail"]["product"][0]["isSellable"]:
                sku["out_of_stock"] = True
            skus[f"{sku['color']}_{sku['size']}"] = sku
        return skus
