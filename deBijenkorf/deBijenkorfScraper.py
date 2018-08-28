import copy
import json
import re
from urllib.parse import urlparse

import scrapy

from deBijenkorf.items import ProductItem, SizeItem


class DeBijenkorfSpider(scrapy.Spider):
    name = 'deBijenkorf'
    api_url = 'https://ceres-catalog.debijenkorf.nl/catalog/product/show?productCode={}&api-version=2.20'
    start_urls = [
        'https://www.debijenkorf.nl/jcr:content.navigation.json'
    ]

    def parse(self, response):
        category_data = json.loads(response.text)
        for level_1 in category_data['categories']:
            cat_1 = level_1['name']
            level_1_url = level_1['url']
            level_2_data = level_1['columns']

            if not level_2_data:
                url = response.urljoin(level_1_url)
                yield scrapy.Request(url, meta={'category': [cat_1], 'link': url},
                                     callback=self.parse_product_listing)

            for level_2 in level_2_data:
                anchor_data = level_2['categories'][0]
                cat_2 = anchor_data['name']
                level_2_url = anchor_data['url']
                level_3_data = anchor_data['children']

                if not level_3_data:
                    url = response.urljoin(level_2_url)
                    yield scrapy.Request(url, meta={'category': [cat_1, cat_2], 'link': url},
                                         callback=self.parse_product_listing)

                for level_3 in level_3_data:
                    cat_3 = level_3['name']
                    level_3_url = level_3['url']
                    url = response.urljoin(level_3_url)
                    yield scrapy.Request(url, meta={'category': [cat_1, cat_2, cat_3], 'link': url},
                                         callback=self.parse_product_listing)

    def parse_product_listing(self, response):
        product_names = response.css('ul.dbk-productlist > li a::attr(name)').extract()

        for product in product_names:
            product_link = self.api_url.format(re.findall('\d{10}', product)[0])
            yield scrapy.Request(product_link, meta=response.meta, callback=self.parse_color)

        url = response.css('.dbk-pagination--next a::attr(href)').extract_first('')
        if url:
            yield scrapy.Request(response.urljoin(url),
                                 meta=response.meta,
                                 callback=self.parse_product_listing)

    def parse_color(self, response):
        product_data = json.loads(response.text)['data']['product']
        product = ProductItem()
        product['skus'] = []
        product['description'] = []
        product['url'] = urlparse(product_data['url'], 'https').geturl()
        product['referrer_url'] = response.meta['link']
        product['retailer_sku'] = product_data['code']
        product['category'] = response.meta['category']
        product['product_name'] = product_data['name']
        product['brand'] = product_data['brand']['name']
        product['currency'] = product_data['sellingPrice']['currencyCode']
        self.extract_description(product, product_data['groupedAttributes'])

        color_list = {}
        image_urls = {}
        for prod in product_data['variantProducts']:
            size_list = color_list.setdefault(prod['color'], [])
            size_list.append(prod)
            image_urls.update({prod['color']: [urlparse(url['url'], 'https').geturl() for url in prod['images']]})

        for color_name, color_data in color_list.items():
            product['color_name'] = color_name
            product['identifier'] = color_data[0]['code'][:-2]
            product['image_urls'] = image_urls[color_name]
            yield from self.parse_size(color_data, copy.deepcopy(product))

    def extract_description(self, product, grouped_attributes):
        for desc_value in grouped_attributes.values():
            product['description'].extend(['{}: {}'.format(element['label'], element['value'])
                                           for element in desc_value])

    def parse_size(self, color_size, product):
        for size in color_size:
            size_item = SizeItem()
            size_item['size_identifier'] = size['code']
            size_item['size_name'] = size['size']
            size_item['full_price'] = size['sellingPrice']['value']
            if size.get('overriddenPrices'):
                size_item['sale_price'] = size.get('overriddenPrices')[0]['value']
            size_item['stock'] = size['availability']['stock']

            product['skus'].append(size_item)
            product['availability'] = any(size['stock'] for size in product['skus'])

        yield product
