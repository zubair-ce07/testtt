import json
import re

import scrapy

from maurices.items import MauricesProduct


class MauricesParseProduct(scrapy.Spider):
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
        product['skus'] = {}
        product['image_urls'] = []
        product_data = response.css('#pdpInitialData::text').extract_first()
        raw_product = json.loads(product_data)['pdpDetail']['product'][0]
        self.add_skus(product, raw_product)
        product['requests'] = self.create_color_requests(raw_product, product)
        yield self.request_or_item(product)

    def parse_color(self, response):
        product = response.meta.get('product')
        image_url_r = 'mauricesProdATG/[^"]*'
        image_url_re = re.compile(image_url_r)
        product['image_urls'].extend(
            list(set(image_url_re.findall(response.body.decode()))))
        yield self.request_or_item(product)

    def request_or_item(self, product):
        requests = product['requests']
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            return request
        del product['requests']
        return product

    def create_color_requests(self, raw_product, product):
        product_id = product['retailer_sku']
        colors = self.attribute_map(raw_product['all_available_colors'])
        requests = []
        for color_id in colors:
            url = self.image_url_t.format(pid=product_id, color_id=color_id)
            requests.append(scrapy.Request(url, callback=self.parse_color))
        return requests

    def add_skus(self, product, raw_product):
        colors = self.attribute_map(raw_product['all_available_colors'])
        sizes = self.attribute_map(raw_product['all_available_sizes'])
        product['category'] = raw_product['ensightenData'][0]['categoryPath']
        available_sku_keys = []
        for raw_sku in raw_product['skus']:
            sku_key = f"{colors.get(raw_sku['color'])}_{sizes.get(raw_sku['size'])}"
            available_sku_keys.append(sku_key)

        for color_id in colors:
            for size_id in sizes:
                sku_key = str(colors[color_id] + '_' + sizes[size_id])
                product['skus'][sku_key] = {
                    'color': colors[color_id],
                    'currency': 'USD',
                    'price': raw_product['all_available_colors'][0]['values'][0]['prices']['sale_price'],
                    'size': sizes[size_id],
                }
                if sku_key not in available_sku_keys:
                    product['skus'][sku_key]['out_of_stock'] = True

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

