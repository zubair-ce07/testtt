import json
import re

from scrapy import Spider
from scrapy import Request

from maurices.items import MauricesProduct


class MauricesParseProduct(Spider):
    name = 'maurices_parse_product'
    image_url_t = 'https://mauricesprodatg.scene7.com/is/image/mauricesProdATG/' \
        '{pid}_{color_id}_ms?req=set,json&id={color_id}'

    def parse_product(self, response):
        product = MauricesProduct()
        product['brand'] = 'maurices'
        product['name'] = self.product_name(response)
        product['description'] = self.product_description(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['url'] = response.url
        product['category'] = self.product_category(response)
        product['skus'] = self.product_skus(response)
        product['image_urls'] = []
        product['requests'] = self.product_color_requests(response)
        yield self.request_or_item(product)

    def parse_color(self, response):
        product = response.meta.get('product')
        image_url_r = 'mauricesProdATG/[^"]*'
        image_url_re = re.compile(image_url_r)
        product['image_urls'].extend(list(set(image_url_re.findall(response.body.decode()))))
        yield self.request_or_item(product)

    def request_or_item(self, product):
        requests = product['requests']
        
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            return request
        
        del product['requests']
        return product

    def available_sku_keys(self, raw_product):
        colors = self.attribute_map(raw_product['all_available_colors'])
        sizes = self.attribute_map(raw_product['all_available_sizes'])
        available_sku_keys = []

        for raw_sku in raw_product['skus']:
            sku_key = f"{colors.get(raw_sku['color'])}_{sizes.get(raw_sku['size'])}"
            available_sku_keys.append(sku_key)
        
        return available_sku_keys

    def product_color_requests(self, response):
        product_id = self.product_retailer_sku(response)
        raw_product = self.raw_product(response)
        colors = self.attribute_map(raw_product['all_available_colors'])
        requests = []
        
        for color_id in colors:
            url = self.image_url_t.format(pid=product_id, color_id=color_id)
            requests.append(Request(url, callback=self.parse_color))
        
        return requests

    def product_skus(self, response):
        raw_product = self.raw_product(response)
        colors = self.attribute_map(raw_product['all_available_colors'])
        sizes = self.attribute_map(raw_product['all_available_sizes'])
        available_sku_keys = self.available_sku_keys(raw_product)
        skus = {}

        for color_id in colors:
            for size_id in sizes:
                sku_key = str(colors[color_id] + '_' + sizes[size_id])
                skus[sku_key] = {
                    'color': colors[color_id],
                    'size': sizes[size_id],
                }
                skus[sku_key].update(self.product_currency_and_price(response))
                
                if sku_key not in available_sku_keys:
                    skus[sku_key]['out_of_stock'] = True
        
        return skus

    def product_currency_and_price(self, response):
        raw_product = self.raw_product(response)
        prices = raw_product['all_available_colors'][0]['values'][0]['prices']
        curr_price = prices['sale_price']
        previous_price = prices['list_price']
        currency_and_price = {
            'currency': 'USD',
            'price': curr_price,
            }

        if curr_price != previous_price:
            currency_and_price['previous_price'] = previous_price
        
        return currency_and_price

    def raw_product(self, response):
        css = '#pdpInitialData::text'
        product_data = response.css(css).extract_first()
        return json.loads(product_data)['pdpDetail']['product'][0]

    def product_category(self, response):
        raw_product = self.raw_product(response)
        return raw_product['ensightenData'][0]['categoryPath']

    def product_name(self, response):
        name_css = '.mar-product-title::text'
        return response.css(name_css).extract_first()

    def product_description(self, response):
        description_css = '.mar-product-description-content li::text'
        return response.css(description_css).extract()

    def product_retailer_sku(self, response):
        return response.url.split('/')[-1]

    def attribute_map(self, all_attributes):
        if not all_attributes:
            return {}

        return {str(attribute['id']): str(attribute['value']) for attribute in all_attributes[0]['values']}

