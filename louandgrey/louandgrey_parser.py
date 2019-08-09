import json
import re

from scrapy.spiders import Spider, Request
from w3lib.url import add_or_replace_parameter

from louandgrey.items import LouandgreyItem


class LouandgreyParser(Spider):
    market = 'US'
    gender = 'women'
    currency = 'USD'
    brand = 'louandgrey'
    name = 'louandgreyparser'
    retailer = 'louandgrey-us'
    product_url = 'https://www.louandgrey.com/cws/catalog/product.jsp'
    image_request_url_t = 'https://anninc.scene7.com/is/image/LO/{}_IS?req=set,json'

    allowed_domains = [
        'louandgrey.com',
        'anninc.scene7.com'
    ]

    def parse(self, response):
        item = LouandgreyItem()
        item['url'] = response.url
        item['trail'] = response.meta.get('trail', [])
        item['brand'] = self.brand
        item['market'] = self.market
        item['gender'] = self.gender
        item['retailer'] = self.retailer
        item['care'] = self.get_care(response)
        item['name'] = self.get_name(response)
        item['category'] = self.get_categories(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['description'] = self.get_description(response)

        requests = self.get_sku_requests(response) + self.get_image_requests(response)
        response.meta['requests'] = requests

        return self.next_request_or_item(item, response)

    def parse_skus(self, response):
        item = response.meta['item']
        item['skus'] = self.get_skus(response)
        return self.next_request_or_item(item, response)

    def parse_image_urls(self, response):
        item = response.meta['item']
        item['image_urls'] = self.get_image_urls(response)
        return self.next_request_or_item(item, response)

    def next_request_or_item(self, item, response):
        if not(response.meta and response.meta.get('requests')):
            return item

        requests = response.meta['requests']
        request = requests.pop(0)
        request.meta.setdefault('item', item)
        request.meta.setdefault('requests', requests)

        return request

    def get_skus(self, response):
        skus = []
        product_details = json.loads(response.text)['products'][0]
        pricing_details = self.get_pricing_details(product_details)

        for raw_skus in product_details['skucolors']['colors']:

            for raw_sku in raw_skus['skusizes']['sizes']:
                if raw_sku['available'] == 'true':
                    sku = {**pricing_details}
                    sku['colour'] = raw_skus['colorName']
                    sku['size'] = raw_sku['sizeAbbr']
                    sku['sku_id'] = raw_sku['skuId']
                    sku['out_of_stock'] = not bool(int(raw_sku['quantity']))
                    skus.append(sku)

        return skus

    def get_sku_requests(self, response):
        url = add_or_replace_parameter(self.product_url, 'prodId', self.get_product_id(response))
        return [Request(url=url, callback=self.parse_skus)]

    def get_image_requests(self, response):
        url = self.image_request_url_t.format(self.get_product_id(response))
        return [Request(url=url, callback=self.parse_image_urls)]

    def get_name(self, response):
        return response.css('h1[itemprop="name"]::text').get()

    def get_product_id(self, response):
        return response.css('input[name="productId"]::attr(value)').get()

    def get_categories(self, response):
        return response.css('.breadcrumb li span[itemprop="name"]::text').getall()[1:-1]

    def get_description(self, response):
        description_css = '.detailsPanel .description::text, .bulletpoint::text'
        return self.sanitize_list(response.css(description_css).getall())

    def get_care(self, response):
        return self.sanitize_list(response.css('#fabricpanel::text').getall())

    def get_image_urls(self, response):
        match = re.search(r'{.*}', response.text)
        if not match:
            return []

        image_url = re.sub(r'LO.*', '', self.image_request_url_t)
        image_items = json.loads(match.group(0))['set']['item']

        if isinstance(image_items, dict):
            return [f'{image_url}{image_items["i"]["n"]}']

        return [f'{image_url}{item["i"]["n"]}' for item in image_items]

    def sanitize_list(self, inputs):
        return [i.strip() for i in inputs if i and i.strip()]

    def sanitize_price(self, price):
        return float(''.join(re.findall(r'\d+', price)))

    def get_pricing_details(self, product_details):
        pricing = {'currency': self.currency}
        pricing['price'] = self.sanitize_price(product_details['listPrice'])

        if product_details.get('salePrice'):
            pricing['price'] = self.sanitize_price(product_details['salePrice'])
            pricing['previous_prices'] = [self.sanitize_price(product_details['listPrice'])]

        return pricing
