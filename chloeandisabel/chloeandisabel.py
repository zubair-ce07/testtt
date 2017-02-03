import json
import re
from scrapy.http.request import Request
from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider


class Mixin:
    allowed_domains = ["www.chloeandisabel.com"]
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
        product_master = self.product_master(product)
        garment['name'] = product_master['name']
        garment['brand'] = 'chloeandisabel'
        garment['image_urls'] = product_master['image_urls']
        garment['gender'] = 'women'
        garment['description'] = self.product_description(product_master)
        garment['category'] = [product_master['category']]
        garment['care'] = self.product_care(product_master)
        if not product_master['in_stock']:
            garment['out_of_stock'] = True
        garment['skus'] = self.skus(product)
        return garment

    def skus(self, product):
        skus = {}
        for variant in product['variantsIncludingMaster']:
            if not variant['is_master']:
                prev_price, price = self.variant_pricing(variant)
                sku = {
                    'color': self.variant_color(variant),
                    'price': price,
                    'currency': variant['localCurrency']['code'],
                    'size': self.one_size,
                }

                if prev_price:
                    sku.update({'previous_prices': [prev_price]})

                if variant['option_values']:
                    option = variant['option_values'][0]
                    if option['option_type']['presentation'] == 'Size':
                        sku.update({'size': option['presentation']})

                if not variant['in_stock']:
                    sku.update({'out_of_stock': True})
                skus[variant['sku']] = sku

        return skus

    def variant_color(self, variant):
        description = [variant['description']]
        props = self.product_properties(variant)
        for x in description + props:
            color = self.detect_colour(x)
            if color:
                return color
        return None

    def product_care(self, product):
        care = []
        for p in self.product_properties(product):
            if self.care_criteria(p):
                care.append(p)
        return care

    def variant_pricing(self, variant):
        price = CurrencyParser.float_conversion(variant['localPrice'])
        if variant['sale_price']:
            sale_price = CurrencyParser.float_conversion(variant['sale_price'])
            return price, sale_price
        return None, price

    def product_description(self, product):
        desc = re.sub('<[^>]+>', '', product['description'])
        desc += '\n'.join(p for p in self.product_properties(product))
        return desc

    def product_properties(self, product):
        return [p['value'] for p in product['displayable_properties']]

    def raw_product(self, response):
        script_elem = response.css('script:contains(initializeCandiReactApp)::text').extract_first()
        json_text = script_elem.replace('initializeCandiReactApp(', '')
        json_text = '[{}]'.format(json_text[:-3])
        return json.loads(json_text)[1]['product']

    def product_master(self, product):
        variants = product["variantsIncludingMaster"]
        return [v for v in variants if v['is_master']].pop()


class ChloeAndIsabelCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = ChloeAndIsabelParseSpider()
    base_url = 'https://www.chloeandisabel.com'

    def parse(self, response):
        json_text = response.text.replace('chloe_isabel_app.loadProducts(', '')
        json_text = json_text[:-2]
        products = json.loads(json_text)
        for product in products:
            if product['sellable']:
                url = product['variantsIncludingMaster'][0]['permalink_path']
                yield Request(url=self.base_url+url, callback=self.parse_item)
