from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean
from ..parsers.jsparser import JSParser

class Mixin:
    retailer = "bettybarclay"
    allowed_domains = ["bettybarclay.com"]
    start_url = "https://www.bettybarclay.com/"

class MixinUK(Mixin):
    retailer = Mixin.retailer + "-uk"
    market = "UK"
    start_urls = [f"{Mixin.start_url}uk/"]


class MixinFR(Mixin):
    retailer = Mixin.retailer + "-fr"
    market = "FR"
    start_urls = [f"{Mixin.start_url}fr/"]


class MixinDE(Mixin):
    retailer = Mixin.retailer + "-de"
    market = "DE"
    start_urls = [f"{Mixin.start_url}de/"]


class MixinAT(Mixin):
    retailer = Mixin.retailer + "-at"
    market = "AT"
    lang = "de"
    start_urls = [f"{Mixin.start_url}at/"]


class MixinNL(Mixin):
    retailer = Mixin.retailer + "-nl"
    market = "NL"
    start_urls = [f"{Mixin.start_url}nl/"]


class BettyBarclayParseSpider(BaseParseSpider):
    price_css = '.articlePrice ::text'

    def parse(self, response):
        raw_product = self.raw_product(response)
        sku_id = raw_product["id"]
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment["name"] = raw_product["name"]
        garment["brand"] = raw_product["brand"]
        garment["category"] = [raw_product["category"]]
        garment["description"] = self.product_description(response)
        garment["care"] = self.product_care(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        garment['meta'] = {
            'requests_queue': self.colour_requests(response) +
                              self.size_requests(response)
        }
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['meta']['requests_queue'] += self.size_requests(response)
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def raw_product(self, response):
        raw_product = response.xpath('//script[contains(text(),"productDetail")]/text()').extract_first()
        return JSParser(raw_product)["d"]["ecommerce"]["detail"]["products"][0]

    def product_description(self, response):
        return clean(response.css('.longDesc ::text'))

    def product_care(self, response):
        return clean(response.css('.careinstr ::text,.material ::text'))

    def image_urls(self, response):
        return clean(response.css('#detailsImageList li::attr(data-zoom-image)'))

    def colour_requests(self, response):
        colour_urls = response.css('.articleVariantBasket .color ::attr(href)').extract()
        return [Request(url=url, callback=self.parse_colour) for url in colour_urls]

    def size_requests(self, response):
        size_urls = response.css('.noncolor ::attr(href)').extract()
        return [Request(url=url, callback=self.parse_size) for url in size_urls]

    def skus(self, response):
        sku = self.product_pricing_common_new(response)
        sku['colour'] = response.css('.articleVariantBasket .currentVariant ::text').extract_first()
        sku['size'] = response.css('.noncolor .active ::attr(data-size)').extract_first()
        sku['size'] = self.one_size if sku['size'] == 'ACC' else sku['size']
        sku_id = f'{sku["colour"]}_{sku["size"]}'
        return {sku_id: sku}


class BettyBarclayCrawlSpider(BaseCrawlSpider):
    listings_css = [
        ".categoryMenu",
        ".manu-navileiste",
        ".pager",
    ]

    products_css = [
        ".productListEntry"
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class UKParseSpider(MixinUK, BettyBarclayParseSpider):
    name = MixinUK.retailer + "-parse"


class UKCrawlSpider(MixinUK, BettyBarclayCrawlSpider):
    name = MixinUK.retailer + "-crawl"
    parse_spider = UKParseSpider()


class FRParseSpider(MixinFR, BettyBarclayParseSpider):
    name = MixinFR.retailer + "-parse"


class FRCrawlSpider(MixinFR, BettyBarclayCrawlSpider):
    name = MixinFR.retailer + "-crawl"
    parse_spider = FRParseSpider()


class DEParseSpider(MixinDE, BettyBarclayParseSpider):
    name = MixinDE.retailer + "-parse"


class DECrawlSpider(MixinDE, BettyBarclayCrawlSpider):
    name = MixinDE.retailer + "-crawl"
    parse_spider = DEParseSpider()


class ATParseSpider(MixinAT, BettyBarclayParseSpider):
    name = MixinAT.retailer + "-parse"


class ATCrawlSpider(MixinAT, BettyBarclayCrawlSpider):
    name = MixinAT.retailer + "-crawl"
    parse_spider = ATParseSpider()


class NLParseSpider(MixinNL, BettyBarclayParseSpider):
    name = MixinNL.retailer + "-parse"


class NLCrawlSpider(MixinNL, BettyBarclayCrawlSpider):
    name = MixinNL.retailer + "-crawl"
    parse_spider = NLParseSpider()

