# -*- coding: utf-8 -*-
import json
import re
import urllib.parse as urlparse
from urllib.parse import urlencode
from copy import deepcopy

from scrapy import Request
from scrapy import Spider

from woolworths.spiders.products import Product


class WoolworthSpider(Spider):
    name = 'woolworth'
    item_per_page = 60
    blacklist_categorires = ['food', 'gift cards', 'size guide', 'lookbooks', 'littleworld', 'today with woolies',
                             'shop by brand', 'brands']

    def start_requests(self):
        start_urls = 'https://www.woolworths.co.za/'
        yield Request(
            url=start_urls,
            callback=self.parse_homepage
        )

    def parse_homepage(self, response):
        raw_data = response.css('script:contains("window.__INITIAL_STATE__")::text').extract_first()
        raw_data = re.findall('= (.*)', raw_data)
        data = json.loads(raw_data[0])

        for level1 in data['header']['meganav']['rootCategories']:
            label1 = level1['categoryName']
            if label1.lower() in self.blacklist_categorires:
                continue

            for level2 in level1['subCategories']:
                label2 = level2['categoryName']
                if label2.lower() in self.blacklist_categorires:
                    continue

                yield Request(
                    url=response.urljoin(level2['categoryURL']),
                    callback=self.parse_pagination,
                    meta={
                        'category': [label1, label2]
                    }
                )

                for level3 in level2.get('subCategories', []):
                    label3 = level3['categoryName']
                    if label3.lower() in self.blacklist_categorires:
                        continue

                    yield Request(
                        url=response.urljoin(level3['categoryURL']),
                        callback=self.parse_pagination,
                        meta={
                            'category': [label1, label2, label3]
                        }
                    )

    def parse_pagination(self, response):
        item_count = response.css('.pagination__info::text').re_first('\d+')
        if not item_count:
            return

        item_count = int(item_count)
        yield from self.parse_products(response)
        if item_count < self.item_per_page:
            return

        nr_param = response.css('.enhanced-select option::attr(value)').extract_first()
        nr_param = re.findall('Nr=(.*)&No', nr_param)
        for page_item_no in range(self.item_per_page, item_count, self.item_per_page):
            params = {
                'No': page_item_no,  # number of the first item on that page
                'Nr': nr_param[0],  # param taken from page under item_per_page option
                'Nrpp': self.item_per_page,
                'Ns': '',
                'Ntt': ''
            }
            url_parts = urlparse.urlparse(response.url)
            params.update({'pageURL': url_parts.path})
            next_url = self.add_query_params(response.urljoin('/server/searchCategory'), params)

            yield Request(
                url=next_url,
                callback=self.parse_products,
                meta=response.meta
            )

    def parse_products(self, response):
        raw_data = response.css('script:contains("window.__INITIAL_STATE__")::text').extract_first()
        if raw_data:  # first listing page from pagination
            raw_data = re.findall('= (.*)', raw_data)
            data = json.loads(raw_data[0])
            data = data['clp']['SLPData'][0]
        else:  # listing page from pagination
            data = json.loads(response.text)
            data = data['contents'][0]
        item_data = data['mainContent'][0]['contents'][0]['records']
        for item in item_data:
            yield Request(
                url=response.urljoin(item['detailPageURL']),
                callback=self.parse_item,
                meta=response.meta
            )

    def parse_item(self, response):
        raw_data = response.css('body script::text').extract_first()
        raw_data = re.findall('= (.*)', raw_data)
        data = json.loads(raw_data[0])
        item_data = data['pdp']
        product_info = item_data['productInfo']
        if not item_data.get('productPrices'):
            return
        temp, product_price = item_data['productPrices'][product_info['productId']].popitem()
        product_price = product_price['skuPrices']

        item = Product()
        item['url'] = response.url
        item['description'] = product_info['longDescription']
        item['name'] = product_info['displayName']
        item['category'] = response.meta['category']

        item['brand'] = product_info['productAttributes'][0]['attributeValue']\
            if product_info['productAttributes'] else None
        item['retailer_sku'] = product_info['productId']
        if product_info['productAttributes']:
            item['care'] = response.urljoin(product_info['productAttributes'][0]['imageURL'])\
                if product_info['productAttributes'][0]['attributeDisplayName'].lower() == 'care' else None

        item['image_urls'] = [image['internalAuxiliaryImage'] for image in product_info['auxiliaryMedia'].values()]
        item['image_urls'] = [response.urljoin(url) for url in item['image_urls']]

        for color in product_info['colourSKUs']:
            color_item = deepcopy(item)
            color_item['color_name'] = color['colour']
            color_id = color['styleId']
            color_item['identifier'] = color_id
            size_info = product_info['styleIdSizeSKUsMap'][color_id]
            yield self.parse_sizes(color_item, size_info, product_price)

    @staticmethod
    def parse_sizes(item, size_info, product_price):
        item['skus'] = {}
        for size in size_info:
            item['skus'].update({
                size['id']: {
                    'currency': 'ZAR',
                    'sale_price': product_price[size['id']]['SalePrice'],
                    'full_price': product_price[size['id']]['ListPrice'],
                    'size_name': size['size']
                }
            })
        return item

    @staticmethod
    def add_query_params(url, params):
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        return urlparse.urlunparse(url_parts)
