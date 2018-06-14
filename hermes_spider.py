import re
import json

from scrapy.link import Link
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, Request

from .base import BaseParseSpider, BaseCrawlSpider, clean


class ProductExtractor():
    def raw_product(self, response):
        xpath = '//script[contains(text(),"Drupal.settings")]/text()'
        raw_product = response.xpath(xpath).re('\{.*\:\{.*\:.*\}\}')[0]
        return json.loads(raw_product)        


class Mixin:
    retailer = 'hermes'
    allowed_domains = ['hermes.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    start_urls = ['https://www.hermes.com/us/en/']


class HermesParseSpider(BaseParseSpider):
    price_css = '.field-type-commerce-price'

    def parse(self, response):
        product = ProductExtractor()
        raw_product = product.raw_product(response)
        sku_id = self.sku_id(response)
        garment = self.new_unique_garment(sku_id)
        common_sku = self.product_pricing_common(response)
        raw_skus = self.raw_skus(self.product(raw_product))
        
        if not garment:
            return
        
        self.boilerplate(garment, response)
        garment['name'] = self.product_name(response)
        garment['care'] = self.product_care(response)
        garment['brand'] = self.product_brand(response)
        garment['description'] = self.product_description(response)
        garment['category'] = self.product_category(raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['image_urls'] = self.image_urls(self.product(raw_product))

        return self.stock_request(raw_skus, garment, raw_product, common_sku)

    def parse_skus(self, response):
        garment = response.meta.get('garment')
        garment['skus'] = self.skus(response)

        yield garment

    def skus(self, response):
        skus = {}
        raw_product = self.product(response.meta.get('raw_product'))
        stock = json.loads(response.text)
        common_sku = response.meta.get('common_sku')

        for product in raw_product:
            sku = common_sku.copy()

            if 'field_color_hermes' in product['attributes']:
                colour = product['attributes']['field_color_hermes']['name'].replace(' ', '-')
                colour = colour.lower().replace('/', '-')
                sku['colour'] = colour

            if 'field_ref_size' in product['attributes']:
                sku['size'] = product['attributes']['field_ref_size']['attr_display']
            else:
                sku['size'] = self.one_size

            if stock[product['sku']]['in_stock'] is False:
                sku['out_of_stock'] = True

            skus[product['sku']] = sku
        
        return skus

    def stock_request(self, raw_skus, garment, raw_product, common_sku):
        stock_url = 'https://www.hermes.com/apps/ecom/stock'
        parameters = {"skus": raw_skus, "locale": "us_en"}
        cookies = {"ECOM_SESS": "b1c9d9f8566e78802fa6eb5325246417"}

        return Request(stock_url, callback=self.parse_skus, method='POST',
                                  body=json.dumps(parameters), 
                                  cookies=cookies,
                                  headers={'content-type': 'application/json'},
                                  meta={'garment': garment, 'raw_product': raw_product,
                                        'common_sku': common_sku})   

    def product(self, raw_product):
        raw_product = raw_product['hermes_products']['data']['products']
        
        if not isinstance(raw_product[0], dict):
            raw_product = raw_product[0]
        
        return raw_product

    def image_urls(self, raw_product):
        return [image['uri'] for product in raw_product for image in product['images']] 

    def product_gender(self, raw_product):
        product_name = raw_product['personalize_taxonomy_context']['vocabularies']['product_category']
        soup = product_name.lower()
        return self.gender_lookup(soup) or 'unisex_adults'

    def raw_description(self, response):
        descp_css = '.field-name-field-description>div::text'
        return clean(response.css(descp_css))

    def sku_id(self, response):
        return clean(response.css('.commerce-product-sku p span::text'))[0]

    def raw_skus(self, raw_product):
        return [prod['sku'] for prod in raw_product]

    def colours(self, raw_products):
        return set([pd['attributes']['field_color_hermes']['name'] for pd in raw_products])

    def product_name(self, response):
        return clean(response.css('#variant-info>h1::text'))

    def product_care(self, response):
        return [pc for pc in self.raw_description(response) if self.care_criteria(pc)]

    def product_description(self, response):
        return [pd for pd in self.raw_description(response) if not self.care_criteria(pd)]

    def product_category(self, raw_product):
        return raw_product['raw_terms_visitor_actions']['pageContext']['Taxonomy']['Product category']


class HermesCrawlSpider(BaseCrawlSpider):
    pagination_url = 'https://www.hermes.com/apps/cde/personalize/grid/{}'

    listing = ['.product-grid-wrap']
    product = ['.filter-results']

    rules = (Rule(LinkExtractor(restrict_css=listing), callback='parse_pagination'),    
             Rule(LinkExtractor(restrict_css=product), callback='parse_item'))

    def parse_pagination(self, response):
        yield from super().parse(response)
        load_more = clean(response.css('.lazy-load::text'))
        
        if not load_more:
            return response.url

        product = ProductExtractor()
        raw_product = product.raw_product(response)
        category = raw_product['hermes_category']['data']
        parameters = {"offset": 36, "limit": 36, "locale": "us_en"}
    
        return Request(self.pagination_url.format(category), headers={'content-type': 'application/json'},
                                                             method='POST',
                                                             body=json.dumps(parameters),
                                                             callback=self.parse_pagination)
     

class HermesUSParseSpider(HermesParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class HermesUSCrawlSpider(HermesCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = HermesUSParseSpider()

