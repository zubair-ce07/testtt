from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = "rebellious"
    allowed_domains = ["www.rebelliousfashion.co.uk"]
    gender = "women"
    MERCH_INFO = ["(30% OFF)"]


class MixinUK(Mixin):
    retailer = Mixin.retailer + "-uk"
    start_urls = ["https://www.rebelliousfashion.co.uk/?___store=gbp"]
    market = "UK"


class MixinEU(Mixin):
    retailer = Mixin.retailer + "-eu"
    start_urls = ["https://www.rebelliousfashion.co.uk/?___store=eur"]
    market = "EU"


class MixinUS(Mixin):
    retailer = Mixin.retailer + "-us"
    start_urls = ["https://www.rebelliousfashion.co.uk/?___store=usd"]
    market = "US"


class RebelliousParseSpider(BaseParseSpider):
    price_css = '.price-box span ::text'
    raw_description_css = '#product_tabs_description_contents ::text'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response)
        garment["merch_info"] = self.merch_info(response)

        if not garment["skus"]:
            garment.update(self.product_pricing_common_new(response))
            garment["out_of_stock"] = True

        return garment

    def product_id(self, response):
        return self.magento_product_id(response)

    def product_name(self, response):
        return clean(response.css('.product-name h1 ::text'))[0]

    def product_brand(self, response):
        return clean(response.css('#logo ::attr(title)'))[0]

    def product_category(self, response):
        return [category for category, url in response.meta.get("trail")]

    def image_urls(self, response):
        return clean(response.css('.swiper-slide img ::attr(src)'))

    def merch_info(self, response):
        merch_info = clean(response.css('.special-price-discount-percentage ::text'))
        return [m for m in self.MERCH_INFO if m in merch_info]

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common_new(response)
        color_css = '//div[@class="std"]//li/text() | //div[@class="std"]//p/text()'
        common_sku["colour"] = clean(response.xpath(color_css))[0]
        spconfig = self.magento_product_data(response)
        raw_skus = self.magento_product_map(spconfig)

        for sku_id, sku_values in raw_skus.items():
            for sku_value in sku_values:
                sku = common_sku.copy()

                if sku_value["titlenew"] == 'Out Of Stock':
                    sku["out_of_stock"] = True
                size = sku_value["label"]
                sku["size"] = self.one_size if size == "One Size" else size
                skus[sku_id] = sku

        return skus


class RebelliousCrawlSpider(BaseCrawlSpider):
    listing_css = [
        'ul[class="level0"]',
        '.next'
    ]
    product_css = ["a.desktopver"]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )


class RebelliousParseSpiderUK(MixinUK, RebelliousParseSpider):
    name = MixinUK.retailer + "-parse"


class RebelliousCrawlSpiderUK(MixinUK, RebelliousCrawlSpider):
    name = MixinUK.retailer + "-crawl"
    parse_spider = RebelliousParseSpiderUK()


class RebelliousParseSpiderEU(MixinEU, RebelliousParseSpider):
    name = MixinEU.retailer + "-parse"


class RebelliousCrawlSpiderEU(MixinEU, RebelliousCrawlSpider):
    name = MixinEU.retailer + "-crawl"
    parse_spider = RebelliousParseSpiderEU()


class RebelliousParseSpiderUS(MixinUS, RebelliousParseSpider):
    name = MixinUS.retailer + "-parse"


class RebelliousCrawlSpiderUS(MixinUS, RebelliousCrawlSpider):
    name = MixinUS.retailer + "-crawl"
    parse_spider = RebelliousParseSpiderUS()
