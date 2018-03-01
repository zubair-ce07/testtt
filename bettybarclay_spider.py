from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean


class MixinUK:
    retailer = "bettybarclay-uk"
    market = "UK"
    allowed_domains = ["bettybarclay.com"]
    start_urls = ["https://www.bettybarclay.com/uk/"]


class MixinFR:
    retailer = "bettybarclay-fr"
    market = "FR"
    lang = "fr"
    allowed_domains = ["bettybarclay.com"]
    start_urls = ["https://www.bettybarclay.com/fr/"]


class MixinDE:
    retailer = "bettybarclay-de"
    market = "DE"
    lang = "de"
    allowed_domains = ["bettybarclay.com"]
    start_urls = ["https://www.bettybarclay.com/de/"]


class MixinAT:
    retailer = "bettybarclay-at"
    market = "AT"
    lang = "de"
    allowed_domains = ["bettybarclay.com"]
    start_urls = ["https://www.bettybarclay.com/at/"]


class MixinNL:
    retailer = "bettybarclay-nl"
    market = "NL"
    lang = "nl"
    allowed_domains = ["bettybarclay.com"]
    start_urls = ["https://www.bettybarclay.com/nl/"]


class BettyBarclayParseSpider(BaseParseSpider):
    price_css = '.articlePrice ::text'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
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

    def product_id(self, response):
        return response.css('.articleNumber ::text').re('(\d+)')[0]

    def product_name(self, response):
        return clean(response.css('.articleTitle h1::text'))[0]

    def product_brand(self, response):
        return response.xpath('//script[contains(text(),"brand")]').re('brand":"(.*?)"')[0]

    def product_category(self, response):
        return clean(response.xpath('//script[contains(text(),"brand")]').re('category":"(.*?)"'))

    def product_description(self, response):
        return clean(response.css('.longDesc ::text'))

    def product_care(self, response):
        return clean(response.css('.careinstr ::text,.material ::text'))

    def image_urls(self, response):
        return response.css('#detailsImageList li::attr(data-zoom-image)').extract()

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
        ".pager"
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
