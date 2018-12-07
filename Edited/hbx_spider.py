import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'hbx'
    allowed_domains = ['hbx.com']
    default_brand = 'HBX'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=GB']


class MixinCN(Mixin):
    retailer = Mixin.retailer + '-cn'
    market = 'CN'
    lang = 'zh'
    start_urls = ['https://www.hbx.com/catalog/settings?country=CN']


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=JP']


class MixinAU(Mixin):
    retailer = Mixin.retailer + '-au'
    market = 'AU'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=AU']


class MixinCA(Mixin):
    retailer = Mixin.retailer + '-ca'
    market = 'CA'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=CA']


class MixinHK(Mixin):
    retailer = Mixin.retailer + '-hk'
    market = 'HK'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=HK']


class MixinTW(Mixin):
    retailer = Mixin.retailer + '-tw'
    market = 'TW'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=TW']


class MixinKR(Mixin):
    retailer = Mixin.retailer + '-kr'
    market = 'KR'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=KR']

class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=US']

class MixinAE(Mixin):
    retailer = Mixin.retailer + '-ae'
    market = 'AE'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=AE']


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    lang = 'en'
    start_urls = ['https://www.hbx.com/catalog/settings?country=DE']


class HbxParseSpider(BaseParseSpider):
    raw_description_css = '.description ::text'
    brand_css = '#product-summary::attr(data-brand)'
    price_css = '.offers .regular-price::text, .offers .sale-price::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)

        return garment

    def product_id(self, response):
        css = '#product-summary::attr(data-id)'
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = '#product-summary::attr(data-name)'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '[ga-event-category="breadcrumbs"]::text'
        return clean(response.css(css))

    def product_gender(self, response):
        soup = self.raw_skus(response)['gender']
        return self.gender_lookup(soupify(soup)) or Gender.ADULTS.value

    def raw_skus(self, response):
        css = '#product-summary ::attr(data-product)'
        return json.loads(clean(response.css(css))[0])

    def image_urls(self, response):
        return [raw_url['_links']['full']['href'] for raw_url in self.raw_skus(response)['images']]

    def skus(self, response):
        skus = {}

        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = colour = self.raw_skus(response)['display_color']

        raw_sizes = self.raw_skus(response)['variants']
        for raw_size in raw_sizes[1:] or raw_sizes:
            sku = common_sku.copy()
            sku['size'] = size = raw_size['_embedded']['size'] or self.one_size

            if not raw_size['is_in_stock']:
                sku['out_of_stock'] = True

            skus[f'{size}_{colour}'] = sku

        return skus


class HbxCrawlSpider(BaseCrawlSpider, Mixin):
    listings_css = [
        '.navigation-section',
        '.next'
    ]
    products_css = '.picture-wrapper'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class HbxUKParseSpider(HbxParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class HbxUKCrawlSpider(HbxCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = HbxUKParseSpider()


class HbxCNParseSpider(HbxParseSpider, MixinCN):
    name = MixinCN.retailer + '-parse'


class HbxCNCrawlSpider(HbxCrawlSpider, MixinCN):
    name = MixinCN.retailer + '-crawl'
    parse_spider = HbxCNParseSpider()


class HbxJPParseSpider(HbxParseSpider, MixinJP):
    name = MixinJP.retailer + '-parse'


class HbxJPCrawlSpider(HbxCrawlSpider, MixinJP):
    name = MixinJP.retailer + '-crawl'
    parse_spider = HbxJPParseSpider()


class HbxAUParseSpider(HbxParseSpider, MixinAU):
    name = MixinAU.retailer + '-parse'


class HbxAUCrawlSpider(HbxCrawlSpider, MixinAU):
    name = MixinAU.retailer + '-crawl'
    parse_spider = HbxAUParseSpider()


class HbxCAParseSpider(HbxParseSpider, MixinCA):
    name = MixinCA.retailer + '-parse'


class HbxCACrawlSpider(HbxCrawlSpider, MixinCA):
    name = MixinCA.retailer + '-crawl'
    parse_spider = HbxCAParseSpider()


class HbxHKParseSpider(HbxParseSpider, MixinHK):
    name = MixinHK.retailer + '-parse'


class HbxHKCrawlSpider(HbxCrawlSpider, MixinHK):
    name = MixinHK.retailer + '-crawl'
    parse_spider = HbxHKParseSpider()


class HbxTWParseSpider(HbxParseSpider, MixinTW):
    name = MixinTW.retailer + '-parse'


class HbxTWCrawlSpider(HbxCrawlSpider, MixinTW):
    name = MixinTW.retailer + '-crawl'
    parse_spider = HbxTWParseSpider()


class HbxKRParseSpider(HbxParseSpider, MixinKR):
    name = MixinKR.retailer + '-parse'


class HbxKRCrawlSpider(HbxCrawlSpider, MixinKR):
    name = MixinKR.retailer + '-crawl'
    parse_spider = HbxKRParseSpider()


class HbxUSParseSpider(HbxParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class HbxUSCrawlSpider(HbxCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = HbxUSParseSpider()


class HbxAEParseSpider(HbxParseSpider, MixinAE):
    name = MixinAE.retailer + '-parse'


class HbxAECrawlSpider(HbxCrawlSpider, MixinAE):
    name = MixinAE.retailer + '-crawl'
    parse_spider = HbxAEParseSpider()


class HbxDEParseSpider(HbxParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class HbxDECrawlSpider(HbxCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = HbxDEParseSpider()
