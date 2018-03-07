import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = "lasula"
    allowed_domains = ["lasula.co.uk"]
    start_url = "https://www.lasula.co.uk/directory/currency/switch/currency/"


class MixinUK(Mixin):
    retailer = Mixin.retailer + "-uk"
    market = "UK"
    start_urls = [f'{Mixin.start_url}GBP/']


class MixinUS(Mixin):
    retailer = Mixin.retailer + "-us"
    market = "US"
    start_urls = [f'{Mixin.start_url}USD/']


class MixinCA(Mixin):
    retailer = Mixin.retailer + "-ca"
    market = "CA"
    start_urls = [f'{Mixin.start_url}CAD/']


class MixinAU(Mixin):
    retailer = Mixin.retailer + "-au"
    market = "AU"
    start_urls = [f'{Mixin.start_url}AUD/']


class MixinNZ(Mixin):
    retailer = Mixin.retailer + "-nz"
    market = "NZ"
    start_urls = [f'{Mixin.start_url}NZD/']


class MixinSE(Mixin):
    retailer = Mixin.retailer + "-se"
    market = "SE"
    start_urls = [f'{Mixin.start_url}SEK/']


class MixinEU(Mixin):
    retailer = Mixin.retailer + "-eu"
    market = "EU"
    start_urls = [f'{Mixin.start_url}EUR/']


class LasulaParseSpider(BaseParseSpider):
    price_css = '.product-type-data .price-box ::text'
    raw_description_css = '#acctab-description+div.panel ::text'

    def parse(self, response):
        raw_product = self.raw_product(response)
        sku_id = raw_product["sku"]
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment["name"] = raw_product["name"]
        garment["category"] = [raw_product["category"] or '']
        garment["brand"] = "LASULA"
        garment["care"] = self.product_care(response)
        garment["description"] = self.product_description(response)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response, raw_product["sku"])
        return garment

    def raw_product(self, response):
        xpath = '//script[contains(text(),"dataLayer")]/text()'
        return json.loads(response.xpath(xpath).re('detail":({.+}?)\}\}')[0])["products"][0]

    def image_urls(self, response):
        return clean(response.css('.img-box a::attr(href)'))

    def skus(self, response, prod_id):
        xpath = '//script[contains(text(),"Product.Config")]/text()'
        raw_sizes = json.loads(response.xpath(xpath).re('options":(\[\{.+\}\])')[0])
        sizes = [rs['label'] for rs in raw_sizes]
        skus = {}
        for size in sizes:
            sku = self.product_pricing_common_new(response)
            sku["size"] = self.one_size if size == "ONE SIZE" else size
            sku_id = f'{prod_id}_{sku["size"]}'
            skus[sku_id] = sku
        return skus


class LasulaCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '#header-nav',
        '.next'
    ]

    products_css = ['.product-name']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class UKParseSpider(MixinUK, LasulaParseSpider):
    name = MixinUK.retailer + "-parse"


class UKCrawlSpider(MixinUK, LasulaCrawlSpider):
    name = MixinUK.retailer + "-crawl"
    parse_spider = UKParseSpider()


class USParseSpider(MixinUS, LasulaParseSpider):
    name = MixinUS.retailer + "-parse"


class USCrawlSpider(MixinUS, LasulaCrawlSpider):
    name = MixinUS.retailer + "-crawl"
    parse_spider = USParseSpider()


class CAParseSpider(MixinCA, LasulaParseSpider):
    name = MixinCA.retailer + "-parse"


class CACrawlSpider(MixinCA, LasulaCrawlSpider):
    name = MixinCA.retailer + "-crawl"
    parse_spider = CAParseSpider()


class AUParseSpider(MixinAU, LasulaParseSpider):
    name = MixinAU.retailer + "-parse"


class AUCrawlSpider(MixinAU, LasulaCrawlSpider):
    name = MixinAU.retailer + "-crawl"
    parse_spider = AUParseSpider()


class NZParseSpider(MixinNZ, LasulaParseSpider):
    name = MixinNZ.retailer + "-parse"


class NZCrawlSpider(MixinNZ, LasulaCrawlSpider):
    name = MixinNZ.retailer + "-crawl"
    parse_spider = NZParseSpider()


class SEParseSpider(MixinSE, LasulaParseSpider):
    name = MixinSE.retailer + "-parse"


class SECrawlSpider(MixinSE, LasulaCrawlSpider):
    name = MixinSE.retailer + "-crawl"
    parse_spider = SEParseSpider()


class EUParseSpider(MixinEU, LasulaParseSpider):
    name = MixinEU.retailer + "-parse"


class EUCrawlSpider(MixinEU, LasulaCrawlSpider):
    name = MixinEU.retailer + "-crawl"
    parse_spider = EUParseSpider()
