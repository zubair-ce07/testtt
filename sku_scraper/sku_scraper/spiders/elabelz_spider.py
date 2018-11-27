import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import Request
from scrapy.selector import Selector

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'elabelz'
    allowed_domains = ['elabelz.com']
    spider_gender_map = [
        ('النساء', Gender.WOMEN.value),
        ('الرجال', Gender.MEN.value),
        ('الاطفال', Gender.KIDS.value),
        ('أولاد', Gender.BOYS.value),
        ('بنات', Gender.GIRLS.value),
    ]
    spider_colour_map = [
        ()
    ]


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    start_urls = ['https://www.elabelz.com/en_us/']
    currency = 'USD'
    lang = 'en'
    size_api_url = 'https://www.elabelz.com/en_uk/marketplace/product/getproducturl/'


class MixinAE(Mixin):
    retailer = Mixin.retailer + '-ae'
    market = 'AE'
    start_urls = ['https://www.elabelz.com/ar_ae']
    retailer_currency = 'AED'
    lang = 'arabic'


class MixinSA(Mixin):
    retailer = Mixin.retailer + '-sa'
    market = 'SA'
    start_urls = ['https://www.elabelz.com/ar_sa']
    retailer_currency = 'SAR'
    lang = 'arabic'


class MixinKW(Mixin):
    retailer = Mixin.retailer + '-kw'
    market = 'KW'
    start_urls = ['https://www.elabelz.com/ar_kw']
    retailer_currency = 'KWD'
    lang = 'arabic'


class MixinEG(Mixin):
    retailer = Mixin.retailer + '-eg'
    market = 'EG'
    start_urls = ['https://www.elabelz.com/ar_qa/']
    retailer_currency = 'EGP'
    lang = 'arabic'


class ElabelzParseSpider(BaseParseSpider):
    default_brand = 'Elabelz'
    price_css = '.price-info .price::text'
    description_css = '.attribute_description_text ul ::text'
    care_css = '#product-attribute-specs-table ::text'

    def parse(self, response):
        product_id = self.product_id(response)

        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        garment['brand'] = self.product_brand(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.sku(response)

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(garment)

        return self.next_request_or_garment(garment)

    def extract_raw_product(self, response):
        raw_product = clean(response.css('body script::text'))[0]
        raw_product = raw_product.strip('dataLayer.push(').strip(');').replace('\'', '\"')
        print(raw_product)
        return json.loads(json.dumps(raw_product))

    def product_id(self, response):
        x = '//th[contains(text(),"SKU ")]/following-sibling::td/text()'
        return clean(response.xpath(x))[0]

    def product_name(self, response):
        return clean(response.css('.productnametop::text'))

    def product_brand(self, response):
        return clean(response.css('.product-name a::text'))

    def product_category(self, response):
        css = '.breadcrumbs a:not([title*="Home"])::text'
        return clean(response.css(css))

    def image_urls(self, response):
        css = '#product-gallery-container img::attr(src)'
        return clean(response.css(css))

    def product_gender(self, garment):
        soup = soupify(garment.get('care') + garment.get('name', []) +
                       garment.get('category') + garment.get('description'))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def sku(self, response):
        skus = {}

        colour = clean(response.css('.Color p::text'))[0]
        sizes = clean(response.css('.Size span::text'))

        common_sku = self.product_pricing_common(response)
        if not common_sku['currency']:
            common_sku['currency'] = self.retailer_currency
        common_sku['colour'] = colour

        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = 'One Size' if size == 'OS' else size
            skus[f'{sku["size"]}_{sku["colour"]}'] = sku

        return skus


class ElabelzCrawlSpider(BaseCrawlSpider):
    listings_css = ['#navbar-collapse-grid', '.pages']
    products_css = ['.product_listing_link']

    deny_listings = ['stationary']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_listings), callback='parse'),
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
