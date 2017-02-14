import json
import re
from scrapy.http.request import Request
from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, CurrencyParser
from functools import reduce


class Mixin:
    allowed_domains = ['www.chloeandisabel.com', 'cloudfront.net']
    start_urls = ['https://d2wsknpdpvwfd3.cloudfront.net/products/us/customer.json.gz']
    market = 'US'
    retailer = 'chloeandisabel-us'

class ChloeAndIsabelParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        product = self.raw_product(response)
        product_id = product['sku']
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate(garment, response)
        garment['name'] = product['master']['name']
        garment['brand'] = 'chloeandisabel'
        garment['category'] = [product['category']]
        garment['gender'] = self.product_gender(product)
        garment['image_urls'] = product['master']['image_urls']
        garment['description'] = self.product_description(product)
        garment['care'] = self.product_care(product)
        if self.out_of_stock(product['master']):
            garment['out_of_stock'] = True
        garment['skus'] = self.skus(product)
        garment['merch_info'] = self.merch_info(product)
        return garment

    def product_gender(self, product):
        return 'men' if 'men' in product['category'].lower() else 'women'

    def skus(self, product):
        skus = {}
        variants = product['variantsIncludingMaster']
        if len(variants) > 1:
            variants = [v for v in variants if not v['is_master']]
        for variant in variants:
            sku = self.variant_pricing_common(variant)
            sku['color'] = self.variant_color(variant)
            size = self.variant_size(variant)
            sku['size'] = size if size else self.one_size
            if self.out_of_stock(variant):
                sku['out_of_stock'] = True
            skus[variant['sku']] = sku
        return skus

    def variant_color(self, variant):
        return '/'.join(clean([self.detect_colour(d) for d in self.raw_description(variant)]))

    def variant_size(self, variant):
        if variant['option_values']:
            value = variant['option_values'][0]
            if value['option_type']['presentation'] == 'Size':
                return value['presentation']

    def product_care(self, product):
        return [d for d in self.raw_description(product['master']) if self.care_criteria(d)]

    def variant_pricing_common(self, variant):
        pricing = {}
        pricing['price'] = CurrencyParser.float_conversion(variant['localPrice'])
        pricing['currency'] = variant['localCurrency']['code']
        if variant['sale_price']:
            pricing['previous_prices'] = CurrencyParser.float_conversion(variant['sale_price'])
        return pricing

    def product_description(self, product):
        return [d for d in self.raw_description(product['master']) if not self.care_criteria(d)]

    def raw_description(self, product):
        desc = self.text_from_html(product['description'])
        desc += [p for p in [d['value'] for d in product['displayable_properties']]]
        return desc

    def raw_product(self, response):
        script_css = 'script:contains(initializeCandiReactApp)::text'
        script_elem = response.css(script_css).extract_first()
        json_text = script_elem.replace('initializeCandiReactApp(', '')
        json_text = '[{}]'.format(json_text[:-3])
        product = json.loads(json_text)[1]['product']
        variants = product["variantsIncludingMaster"]
        product['master'] = [v for v in variants if v['is_master']].pop()
        return product

    def merch_info(self, product):
        return product.get('promotion_messages', [])

    def out_of_stock(self, product):
        return not product['in_stock']


class ChloeAndIsabelCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = ChloeAndIsabelParseSpider()
    base_url = 'https://www.chloeandisabel.com'

    def parse(self, response):
        json_re = 'chloe_isabel_app.loadProducts\((.*)\);'
        raw_json = re.findall(json_re, response.text)[0]
        products = json.loads(raw_json)
        for product in products:
            url = product['variantsIncludingMaster'][0]['permalink_path']
            meta = {'trail': self.add_trail(response)}
            yield Request(url=self.base_url + url, meta=meta, callback=self.parse_item)

