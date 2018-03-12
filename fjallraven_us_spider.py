import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'fjallraven'


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    allowed_domains = ['fjallraven.us']
    start_urls = ['https://www.fjallraven.us']
    currency = 'USD'
    gender_map = [
        ('Womens', 'women'),
        ('womens', 'women'),
        ('Mens', 'men'),
        ('mens', 'men'),
        ('Kids', 'unisex-kids'),
        ('kids', 'unisex-kids')
    ]


class ParseSpider(BaseParseSpider):

    def parse(self, response):
        pid = self.product_id(response)

        garment = self.new_unique_garment(pid)
        if not garment:
            return

        product = self.raw_product(response)
        self.boilerplate(garment, response)

        garment['brand'] = self.product_brand(product)
        garment['name'] = self.product_name(product)
        garment['description'] = self.product_description(product)
        garment['care'] = self.product_care(product)
        garment['category'] = self.product_category(product)
        garment['gender'] = self.product_gender(product)
        garment['skus'] = self.skus(product)
        garment['image_urls'] = self.image_urls(product)
        return garment

    def raw_product(self, response):
        css = f'script#ProductJson-{self.product_id(response)} ::text'
        raw_js = clean(response.css(css))[0]
        return json.loads(raw_js)

    def product_id(self, response):
        return clean(response.css('[data-section-type="product"] ::attr(data-section-id)'))[0]

    def product_name(self, product):
        return product['title']

    def product_brand(self, product):
        return product['vendor']

    def product_category(self, product):
        return [product['type']]

    def product_gender(self, product):
        for gender_str, gender in self.gender_map:
            if gender_str in product['tags']:
                return gender
        return 'unisex-adults'

    def raw_description(self, product):
        return self.text_from_html(product['description'], xpath='//text()[not(parent::h1)]')

    def product_description(self, product):
        return [d for d in self.raw_description(product) if not self.care_criteria(d)]

    def product_care(self, product):
        return [c for c in self.raw_description(product) if self.care_criteria(c)]

    def skus(self, product):
        skus = {}
        for variant in product['variants']:
            sku = {}
            sku['colour'] = variant['option1']
            sku['size'] = variant['option2'] or self.one_size
            sku['price'] = variant['price']
            sku['currency'] = self.currency
            if not variant['inventory_quantity']:
                sku['out_of_stock'] = True
            skus[variant['id']] = sku

        return skus

    def image_urls(self, product):
        return product['images']


class CrawlSpider(BaseCrawlSpider):
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 2.5,
    # }

    listings_css = [
        '.jetmenu',
        '.pagination',
    ]

    products_css = '.grid-view-item__link'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class ParseSpiderUS(ParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class CrawlSpiderUS(CrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = ParseSpiderUS()
