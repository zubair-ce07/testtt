import json

import scrapy

from maurices.items import MauricesProduct


class MauricesParseProduct(scrapy.Spider):
    name = 'maurices_parse_product'
    product_sku_url = 'https://www.maurices.com/maurices/baseAjaxServlet?'

    def parse_product(self, response):
        product = MauricesProduct()
        product['brand'] = 'maurices'
        product['name'] = self.product_name(response)
        product['description'] = self.product_description(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['url'] = response.url
        product['skus'] = {}
        id = response.url.split('/')[-1]
        url = self.product_sku_url
        url += f'pageId=PDPGetProduct&Action=PDP.getProduct&id={id}'
        yield scrapy.Request(url, callback=self.find_and_append_skus, meta={'product': product})

    def product_name(self, response):
        name_css = '.mar-product-title::text'
        return response.css(name_css).extract_first()

    def product_description(self, response):
        description_css = '.mar-product-description-content li::text'
        return response.css(description_css).extract()

    def product_retailer_sku(self, response):
        return response.url.split('/')[-1]

    def product_image_url(self, product_detail):
        image_urls = []
        for color in product_detail['all_available_colors'][0]['values']:
            image_urls.append(color['sku_image'])
        return image_urls

    def find_and_append_skus(self, response):
        product = response.meta.get('product')
        product_detail = json.loads(response.body)['product'][0]
        product['image_urls'] = self.product_image_url(product_detail)
        self.add_skus(product, product_detail)
        yield product

    def attribute_map(self, attribute_list):
        attributes = dict()
        if attribute_list:
            for attribute in attribute_list[0]['values']:
                attributes[str(attribute['id'])] = attribute['value']
        return attributes

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
                    'out_of_stock': True
                }
        for sku in product_detail['skus']:
            color_id = sku['color']
            size_id = sku['size']
            sku_key = str(colors[color_id] + '_' + sizes[size_id])
            if sku_key in sku_keys:
                sku_keys.remove(sku_key)
        for sku_key in sku_keys:
            product['skus'][sku_key]['out_of_stock'] = True

