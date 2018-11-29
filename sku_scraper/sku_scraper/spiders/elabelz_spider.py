from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'elabelz'
    allowed_domains = ['elabelz.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    start_urls = ['https://www.elabelz.com/en_us/']


class MixinAE(Mixin):
    retailer = Mixin.retailer + '-ae'
    market = 'AE'
    start_urls = ['https://www.elabelz.com/ar_ae']
    lang = 'ar'


class MixinSA(Mixin):
    retailer = Mixin.retailer + '-sa'
    market = 'SA'
    start_urls = ['https://www.elabelz.com/ar_sa']
    lang = 'ar'


class MixinKW(Mixin):
    retailer = Mixin.retailer + '-kw'
    market = 'KW'
    start_urls = ['https://www.elabelz.com/ar_kw']
    lang = 'ar'


class MixinEG(Mixin):
    retailer = Mixin.retailer + '-eg'
    market = 'EG'
    start_urls = ['https://www.elabelz.com/ar_qa/']
    lang = 'ar'


class ElabelzParseSpider(BaseParseSpider):
    default_brand = 'Elabelz'
    price_css = '.price-box ::text'
    brand_css = '.product-name a::text'
    raw_description_css = '.attribute_description_text ul ::text, '\
                          '#product-attribute-specs-table ::text'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['gender'] = self.product_gender(garment)

        return garment

    def product_id(self, response):
        css = '#product-attribute-specs-table :contains(SKU) ~ td::text'
        return clean(response.css(css))[0]

    def product_name(self, response):
        return clean(response.css('.productnametop::text'))[0]

    def product_category(self, response):
        css = '.breadcrumbs a::text'
        return clean(response.css(css))[1:]

    def image_urls(self, response):
        css = '#product-gallery-container img::attr(src)'
        return clean(response.css(css))

    def product_gender(self, garment):
        soup = soupify([garment['name']] + garment['category'] + garment['description'])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, response):
        skus = {}

        colour = clean(response.css('.Color p::text'))[0]

        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = colour

        for size in clean(response.css('.Size span::text')):
            sku = common_sku.copy()
            sku['size'] = self.one_size if size == 'OS' else size
            skus[f'{sku["size"]}_{colour}'] = sku

        return skus


class ElabelzCrawlSpider(BaseCrawlSpider):
    listings_css = ['#navbar-collapse-grid', '.pages']
    products_css = ['.product_listing_link']

    deny_re = ['stationary']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )


class ElabelzUSParseSpider(ElabelzParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class ElabelzUSCrawlSpider(ElabelzCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = ElabelzUSParseSpider()


class ElabelzAEParseSpider(ElabelzParseSpider, MixinAE):
    name = MixinAE.retailer + '-parse'


class ElabelzAECrawlSpider(ElabelzCrawlSpider, MixinAE):
    name = MixinAE.retailer + '-crawl'
    parse_spider = ElabelzAEParseSpider()


class ElabelzSAParseSpider(ElabelzParseSpider, MixinSA):
    name = MixinSA.retailer + '-parse'


class ElabelzSACrawlSpider(ElabelzCrawlSpider, MixinSA):
    name = MixinSA.retailer + '-crawl'
    parse_spider = ElabelzSAParseSpider()


class ElabelzKWParseSpider(ElabelzParseSpider, MixinKW):
    name = MixinKW.retailer + '-parse'


class ElabelzKWCrawlSpider(ElabelzCrawlSpider, MixinKW):
    name = MixinKW.retailer + '-crawl'
    parse_spider = ElabelzKWParseSpider()


class ElabelzEGParseSpider(ElabelzParseSpider, MixinEG):
    name = MixinEG.retailer + '-parse'


class ElabelzEGCrawlSpider(ElabelzCrawlSpider, MixinEG):
    name = MixinEG.retailer + '-crawl'
    parse_spider = ElabelzEGParseSpider()
