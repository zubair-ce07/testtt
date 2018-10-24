import json
import re

import scrapy

from maurices.items import MauricesProduct


class MauricesParseProduct(scrapy.Spider):
    name = 'maurices_parse_product'
    image_url_t = 'https://mauricesprodatg.scene7.com/is/image/mauricesProdATG/'

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
        product_detail = json.loads(product_data)['pdpDetail']['product'][0]
        self.add_skus(product, product_detail)
        color_urls = self.create_image_requests(
            product_detail, product['retailer_sku'])
        yield scrapy.Request(color_urls.pop(), callback=self.parse_colors,
                             meta={'product': product, 'color_urls': color_urls})

    def parse_colors(self, response):
        product = response.meta.get('product')
        image_url_r = re.compile(
            'mauricesProdATG/[0-9]+_C[0-9]+(?:_alt1|_Back)?')
        product['image_urls'].extend(
            list(set(image_url_r.findall(str(response.body)))))
        color_urls = response.meta.get('color_urls')
        if color_urls:
            yield scrapy.Request(color_urls.pop(), callback=self.parse_colors,
                                 meta={'product': product, 'color_urls': color_urls})
        else:
            yield product

    def create_image_requests(self, product_detail, product_id):
        colors = self.attribute_map(product_detail['all_available_colors'])
        urls = [self.image_url_t +
                f'{product_id}_{color_id}_ms?req=set,json&id={color_id}' for color_id in colors]
        return urls

    def add_skus(self, product, product_detail):
        colors = self.attribute_map(product_detail['all_available_colors'])
        sizes = self.attribute_map(product_detail['all_available_sizes'])
        product['category'] = product_detail['ensightenData'][0]['categoryPath']
        sku_keys = []
        for color_id in colors:
            for size_id in sizes:
                sku_key = str(colors[color_id] + '_' + sizes[size_id])
                sku_keys.append(sku_key)
                product['skus'][sku_key] = {
                    'color': colors[color_id],
                    'currency': 'USD',
                    'price': product_detail['all_available_colors'][0]['values'][0]['prices']['sale_price'],
                    'size': sizes[size_id],
                }
        for sku in product_detail['skus']:
            color_id = sku['color']
            size_id = sku['size']
            sku_key = str(colors[color_id] + '_' + sizes[size_id])
            if sku_key in sku_keys:
                sku_keys.remove(sku_key)
        for sku_key in sku_keys:
            product['skus'][sku_key]['out_of_stock'] = True

    def product_name(self, response):
        name_css = '.mar-product-title::text'
        return response.css(name_css).extract_first()

    def product_description(self, response):
        description_css = '.mar-product-description-content li::text'
        return response.css(description_css).extract()

    def product_retailer_sku(self, response):
        return response.url.split('/')[-1]

    def attribute_map(self, attribute_list):
        attributes = dict()
        if attribute_list:
            for attribute in attribute_list[0]['values']:
                attributes[str(attribute['id'])] = str(attribute['value'])
        return attributes

