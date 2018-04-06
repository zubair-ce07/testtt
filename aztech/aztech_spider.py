import json

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class MixinUS:
    retailer = "aztech-us"
    start_urls = ["https://aztechmountain.com/"]
    allowed_domains = ["aztechmountain.com"]
    market = "US"
    gender = "men"


class AztechParseSpider(BaseParseSpider):
    raw_description_css = "div.product__description ::text, .product__tabs__tech-list li ::text"

    def parse(self, response):
        raw_product = self.raw_product(response)
        pid = raw_product["id"]
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_minimal(garment, response)
        garment["category"] = raw_product["tags"]
        garment["name"] = raw_product["title"]
        garment["brand"] = raw_product["vendor"]
        garment["description"] = self.product_description(response)
        garment["care"] = self.product_care(response)
        garment["image_urls"] = self.image_urls(raw_product, response)
        garment["skus"] = self.skus(raw_product, response)

        return garment

    def image_urls(self, raw_product, response):
        return [response.urljoin(image_url) for image_url in raw_product["images"]]

    def skus(self, raw_product, response):
        skus = {}
        currency = clean(response.css('[property="og:price:currency"] ::attr(content)'))[0]

        for raw_sku in raw_product["variants"]:
            money_strs = [raw_product["price"], raw_product["compare_at_price"], currency]
            sku = self.product_pricing_common_new(None, money_strs=money_strs, is_cents=True).copy()

            if not raw_sku["available"]:
                sku["out_of_stock"] = True
            sku["colour"] = raw_sku["option1"]
            sku["size"] = raw_sku["option2"]
            skus[raw_sku["id"]] = sku

        return skus

    def raw_product(self, response):
        xpath = '//script[contains(text(),"initProduct")]/text()'
        raw_json = clean(response.xpath(xpath).re_first('product: (.+),'))
        return json.loads(raw_json)


class AztechCrawlSpider(BaseCrawlSpider):

    listing_css = [
        '.sidebar-nav__sub-links'
    ]

    product_css = ["h3.product-item__title"]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )


class AztechParseSpiderUS(MixinUS, AztechParseSpider):
    name = MixinUS.retailer + "-parse"


class AztechCrawlSpiderUS(MixinUS, AztechCrawlSpider):
    name = MixinUS.retailer + "-crawl"
    parse_spider = AztechParseSpiderUS()
