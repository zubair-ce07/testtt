import json
from w3lib.url import add_or_replace_parameters

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender, soupify


class Mixin:
    retailer = "burberry"
    default_brand = "Burberry"


class MixinCN(Mixin):
    retailer = Mixin.retailer + "-cn"
    market = "CN"
    start_urls = ["https://cn.burberry.com"]
    allowed_domains = ["cn.burberry.com"]

    product_url_t = "https://cn.burberry.com/service/products{0}-p{1}"


class ParseSpider(BaseParseSpider):
    raw_description_css = ".accordion-tab_content ::text"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["gender"] = self.product_gender(garment)
        garment["image_urls"] = []
        garment["skus"] = {}

        garment["meta"] = {
            'requests_queue': self.color_requests(response)
        }

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = ".accordion-tab_content ::text"
        return clean(response.css(css))[-1].split(" ")[1]

    def product_name(self, response):
        css = ".product-purchase_name ::text"
        return clean(response.css(css))[0]

    def product_category(self, response):
        category = clean(response.css(".guest::attr(data-atg-category)"))[0]
        return category.split("/") if category else []

    def product_gender(self, garment):
        soup = soupify(garment["category"], garment["name"])
        return self.gender_lookup(soup, True) or Gender.ADULTS.value

    def image_urls(self, raw_skus):
        return clean([image.get("img", {}).get("src") for image in raw_skus["hdCarousel"]])

    def color_requests(self, response):
        requests = []
        colours_css = ".product-purchase_option::attr(data-id), .guest::attr(data-product-id)"

        colours = clean(response.css(colours_css))
        product_url = clean(response.css(".guest::attr(data-default-url)"))[0].rsplit("-", 1)[0]
        category_id = clean(response.css(".guest::attr(data-atg-category-id)"))[0]
        headers = {'x-csrf-token': clean(response.css(".csrf-token::attr(value)"))[0]}

        for colour in colours:
            url = self.product_url_t.format(product_url, colour)
            add_or_replace_parameters(url, {'id': colour, 'categoryId': category_id})
            requests.append(Request(url, callback=self.parse_color, dont_filter=True, headers=headers))

        return requests

    def parse_color(self, response):
        garment = response.meta["garment"]
        raw_skus = json.loads(response.text)
        garment["skus"].update(self.skus(raw_skus))
        garment["image_urls"] += self.image_urls(raw_skus)
        return self.next_request_or_garment(garment)

    def skus(self, raw_skus):
        skus = {}
        store = raw_skus["findInStore"]
        money_strs = [
            raw_skus["currency"], raw_skus["dataDictionaryProductInfo"]["price"],
            raw_skus["dataDictionaryProductInfo"]["priceDiscount"]
        ]

        common_sku = self.product_pricing_common(None, money_strs=money_strs)
        raw_sizes = store["size"]["items"] if "size" in store else [{"label": self.one_size}]

        colour = raw_skus["dataDictionaryProductInfo"]["color"]
        if colour:
            common_sku["colour"] = colour

        for size in raw_sizes:
            sku = common_sku.copy()
            sku["size"] = size["label"]

            if not size.get("isAvailable", True) or raw_skus["isOutOfStock"]:
                sku["out_of_stock"] = True

            sku_id = f"{sku['colour']}_{sku['size']}" if colour else sku["size"]
            skus[sku_id] = sku

        return skus


class CrawlSpider(BaseCrawlSpider):
    listings_css = [".nav-level2"]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse_pagination"),
    )

    def parse_pagination(self, response):
        pagination_urls = clean(response.css(".shelf::attr(data-all-products)"))
        headers = {'x-csrf-token': clean(response.css(".csrf-token::attr(value)"))[0]}
        meta = {'trail': self.add_trail(response)}

        for url in pagination_urls:
            yield response.follow(url, callback=self.parse_category, headers=headers, meta=meta.copy())

    def parse_category(self, response):
        meta = {'trail': self.add_trail(response)}

        for product in json.loads(response.text):
            yield response.follow(product["link"], callback=self.parse_item, meta=meta.copy())


class ParseSpiderCN(MixinCN, ParseSpider):
    name = MixinCN.retailer + "-parse"


class CrawlSpiderCN(MixinCN, CrawlSpider):
    name = MixinCN.retailer + "-crawl"
    parse_spider = ParseSpiderCN()
