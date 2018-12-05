import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    retailer = 'aloyoga'
    default_brand = 'Alo Yoga'
    spider_one_sizes = ['1']
    merch_info_map = [
        ('limited-edition', 'Limited Edition')
    ]


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    allowed_domains = [
        'www.aloyoga.com'
    ]
    start_urls = [
        'https://www.aloyoga.com/'
    ]


class AloYogaParseSpider(BaseParseSpider):
    price_css = '.main-product-info .price-discount ::text, ' \
                '.main-product-info .price-old ::text'
    raw_description_css = '#description ::text'
    care_css = '#fit p::text'

    def parse(self, response):
        raw_product = self.raw_product(response)
        product_id = self.product_id(raw_product)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = self.product_name(raw_product)
        garment['merch_info'] = self.merch_info(garment)
        garment['care'] = self.product_care(response)
        garment['description'] = self.product_description(response)
        garment['category'] = self.product_category(response)
        garment['brand'] = self.product_brand(raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(response)

        return garment

    def product_id(self, raw_product):
        return raw_product['id']

    def raw_product(self, response):
        css = "script:contains('json_product')"
        return json.loads(response.css(css).re('{.*}')[0])

    def product_name(self, raw_product):
        return raw_product['title']

    def product_category(self, response):
        return clean(response.css('.breadcrumb ::text'))[1:-1]

    def product_brand(self, raw_product):
        return raw_product['vendor']

    def image_urls(self, raw_product):
        return raw_product['images']

    def product_gender(self, raw_product):
        soup = raw_product['type']
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def merch_info(self, garment):
        soup = garment['name'].lower()
        return [merch for merch_str, merch in self.merch_info_map if merch_str in soup]

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        skus = {}

        for raw_sku in self.raw_product(response)['variants']:
            sku = common_sku.copy()
            sku['colour'] = raw_sku['option1']
            sku['size'] = raw_sku['option2']

            if not raw_sku['available']:
                sku['out_of_stock'] = True

            skus[raw_sku['id']] = sku

        return skus


class AloYogaCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.nav-link.nav-link-main',
        '.pagination'
    ]
    products_css = [
        '.product-list-wrapper'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class AloYogaParseSpiderUS(AloYogaParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class AloYogaCrawlSpiderUS(AloYogaCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = AloYogaParseSpiderUS()
