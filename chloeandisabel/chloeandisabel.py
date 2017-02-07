import json
import re
from scrapy.http.request import Request
from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, CurrencyParser
from functools import reduce


class Mixin:
    allowed_domains = ['www.chloeandisabel.com', 'cloudfront.net']
    start_urls = ['https://www.chloeandisabel.com/shop/']
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
        garment['description'] = self.product_description(product_master)
        garment['care'] = self.product_care(product_master)
        if not product_master['in_stock']:
            garment['out_of_stock'] = True
        garment['skus'] = self.skus(product)
        if product['promotion_messages']:
            garment['merch_info'] = self.merch_info(product)
        return garment

    def skus(self, product):
        skus = {}
        if product['availableVariants']:
            variants = [variant for variant in product['variantsIncludingMaster']
                        if not variant['is_master']]
        else:
            variants = [product['variantsIncludingMaster'][0]]
        for variant in variants:
            prev_price, price = self.variant_pricing(variant)
            sku = {
                'color': self.variant_color(variant),
                'price': price,
                'currency': variant['localCurrency']['code'],
                'size': self.one_size,
            }
            if prev_price:
                sku['previous_prices'] = [prev_price]

            if variant['option_values']:
                option = variant['option_values'][0]
                if option['option_type']['presentation'] == 'Size':
                    sku['size'] = option['presentation']

            if not variant['in_stock']:
                sku['out_of_stock'] = True
            skus[variant['sku']] = sku
        return skus

    def variant_sku(self, variant):
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
                sku['size'] = option['presentation']

        if not variant['in_stock']:
            sku['out_of_stock'] = True
        return {variant['sku']: sku}

    def variant_color(self, variant):
        description = [variant['description']]
        props = self.product_properties(variant)
        for x in description + props:
            color = self.detect_colour(x)
            if color:
                return color
        return None

    def product_care(self, product):
        return [d for d in self.raw_description(product) if self.care_criteria(d)]

    def variant_pricing(self, variant):
        price = CurrencyParser.float_conversion(variant['localPrice'])
        if variant['sale_price']:
            sale_price = CurrencyParser.float_conversion(variant['sale_price'])
            return price, sale_price
        return None, price

    def product_description(self, product):
        return [d for d in self.raw_description(product) if not self.care_criteria(d)]

    def raw_description(self, product):
        desc = self.text_from_html(product['description'])
        desc += [p for p in self.product_properties(product)]
        return desc

    def product_properties(self, product):
        return [p['value'] for p in product['displayable_properties']]

    def raw_product(self, response):
        script_css = 'script:contains(initializeCandiReactApp)::text'
        script_elem = response.css(script_css).extract_first()
        json_text = script_elem.replace('initializeCandiReactApp(', '')
        json_text = '[{}]'.format(json_text[:-3])
        return json.loads(json_text)[1]['product']

    def product_master(self, product):
        variants = product["variantsIncludingMaster"]
        return [v for v in variants if v['is_master']].pop()

    def merch_info(self, product):
        return product['promotion_messages']


class ChloeAndIsabelCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = ChloeAndIsabelParseSpider()
    base_url = 'https://www.chloeandisabel.com'
    products_url = 'https://d2wsknpdpvwfd3.cloudfront.net/products/us/customer.json.gz'

    def parse(self, response):
        script_css = 'script:contains(initializeCandiReactApp)::text'
        script = response.css(script_css).extract_first()
        json_text = '[{}]'.format(script.replace('initializeCandiReactApp(', '')[:-3])
        app_json = json.loads(json_text)
        taxons = app_json[0]['taxons']
        slugs = [{u['slug']: u['name'] for u in t['children']} for t in taxons]
        self.collection_slugs = reduce(lambda t, u: t.update(u) or t, slugs)
        return Request(url=self.products_url, callback=self.parse_json)

    def parse_json(self, response):
        products = self.get_products(response)
        for product in products:
            if product['sellable']:
                url = product['variantsIncludingMaster'][0]['permalink_path']
                meta = {
                    'category': self.product_categories(product),
                    'gender': self.product_gender(product),
                    'trail': self.add_trail(response),
                }
                yield Request(url=self.base_url + url, meta=meta, callback=self.parse_item)

    def get_products(self, response):
        json_re = 'chloe_isabel_app.loadProducts\((.*)\);'
        json_text = re.findall(json_re, response.text)[0]
        return json.loads(json_text)

    def product_categories(self, product):
        slugs = [slug['name'] for slug in product['collection_slugs']]
        return [self.collection_slugs[slug] for slug in slugs
                if self.collection_slugs.get(slug)]

    def product_gender(self, product):
        categories = self.product_categories(product)
        return 'men' if "Men's Shop" in categories else 'women'

