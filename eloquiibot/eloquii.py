import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request

from eloquiibot.items import EloquiiProduct


class EloquiiSpider(CrawlSpider):
    name = 'eloquii'
    allowed_domains = ['www.eloquii.com']
    start_urls = ['https://www.eloquii.com']
    merch_map = [
        ("limited edition", "Limited Edition"),
        ("special edition", "Special Edition")
    ]
    sku_req_url_t = "https://www.eloquii.com/on/demandware.store/Sites-eloquii-Site/default/Product-GetVariants?" \
                    "pid={}&format=json"

    listings_css = ['#nav_menu', '.row.justify-content-center.mt-5']
    products_css = ".product-images"

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback="parse_product")
    )

    def parse_product(self, response):
        product = EloquiiProduct()
        if not self.is_available(response):
            return
        product["product_id"] = self.product_id(response)
        product["brand"] = 'Eloquii'
        product["name"] = self.product_name(response)
        product["category"] = self.product_category(response)
        product["description"] = self.product_description(response)
        product["url"] = response.url
        product["image_urls"] = self.image_urls(response)
        product["skus"] = {}
        product["merch_info"] = self.merch_info(product)
        if self.is_out_of_stock(response):
            product["out_of_stock"] = True
            return
        yield Request(url=self.sku_req_url_t.format(product["product_id"]),
                      callback=self.parse_skus, meta={"product": product})

    def product_id(self, response):
        css = "#yotpo-bottomline-top-div::attr(data-product-id)"
        return response.css(css).extract_first()

    def product_name(self, response):
        css = "#yotpo-bottomline-top-div::attr(data-name)"
        return response.css(css).extract_first()

    def product_category(self, response):
        css = "#yotpo-bottomline-top-div::attr(data-bread-crumbs)"
        return response.css(css).extract_first()

    def product_description(self, response):
        css = "[name=description]::attr(content)"
        return response.css(css).extract_first()

    def image_urls(self, response):
        raw_images_data = response.css("#bt_pdp_main > script::text").extract_first()
        raw_images_data = re.sub(r"[\n\t\r]","",raw_images_data)
        images_data = re.findall(r'\"large\" :\[.*?\]', raw_images_data)
        return [re.findall(r'{\"url\" : \"(.*?\.jpg)\",.*?}', images) for
                images in images_data]

    def merch_info(self, product):
        soup = ' '.join(product["name"] + product["description"]).lower()
        merch_info = [merch for merch_str, merch in self.merch_map if merch_str in soup]
        return merch_info

    def is_available(self, response):
        return not bool(re.search(r'\'COMINGSOON\': (true)', response.text))

    def is_out_of_stock(self, response):
        availability = response.css("[property='og:availability']::attr(content)").extract_first()
        return not availability == "IN_STOCK"

    def parse_skus(self, response):
        product = response.meta["product"]
        json_data = json.loads(response.text)
        json_data = json_data["variations"]["variants"]
        product["skus"] = self.skus(json_data)
        yield product

    def skus(self, json_data):
        skus = {}
        for data in json_data:
            sku = self.product_pricing(data)
            sku['color'] = data["attributes"]["colorCode"]
            sku['size'] = data["attributes"]["size"]
            if not data["inStock"]:
                sku["out_of_stock"] = not data["inStock"]
            skus['_'.join(data["attributes"].values())] = sku
        return skus

    def product_pricing(self, json_data):
        prices = {}
        previous_price = json_data["pricing"]["standard"]
        prices["price"] = json_data["pricing"]["sale"]
        prices["currency"] = '$'
        if previous_price != prices["price"]:
            prices["previous_price"] = previous_price
        return prices
