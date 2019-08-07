import json
import re

from scrapy.spiders import Spider, Request
from w3lib.url import add_or_replace_parameter

from louandgrey.items import LouandgreyItem


class LouandgreyParser(Spider):
    market = 'US'
    gender = 'women'
    currency = 'USD'
    name = 'louandgreyparser'
    retailer = 'louandgrey-us'
    product_url = 'https://www.louandgrey.com/cws/catalog/product.jsp'
    image_url = 'https://anninc.scene7.com/is/image/LO/{}_IS?req=set,json'

    allowed_domains = [
        'louandgrey.com',
        'anninc.scene7.com'
    ]

    def parse(self, response):
        item = LouandgreyItem()
        item['url'] = response.url
        item['market'] = self.market
        item['gender'] = self.gender
        item['retailer'] = self.retailer
        item['care'] = self.get_care(response)
        item['name'] = self.get_name(response)
        item['trail'] = response.meta.get('trail', [])
        item['category'] = self.get_categories(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['description'] = self.get_description(response)
        response.meta['requests'] = self.get_sku_requests(item['retailer_sku'])

        return self.next_request_or_item(item, response)

    def next_request_or_item(self, item, response):
        requests = response.meta.get('requests', [])

        if not requests:
            return item

        request = requests.pop(0)
        request.meta.setdefault('item', item)
        request.meta.setdefault('requests', requests)

        return request

    def parse_skus(self, response):
        item = response.meta['item']
        item['skus'] = self.get_skus(response)
        response.meta['requests'].extend(self.get_image_requests(item['retailer_sku']))

        return self.next_request_or_item(item, response)

    def parse_image_urls(self, response):
        item = response.meta['item']
        item['image_urls'] = self.get_image_urls(response)

        yield item

    def get_skus(self, response):
        skus = []
        json_response = json.loads(response.text)
        product_details = json_response['products'][0]
        sku = self.get_pricing_details(product_details)

        for colour_skus in product_details['skucolors']['colors']:
            sku['colour'] = colour_skus['colorName']

            for size in colour_skus['skusizes']['sizes']:
                if size['available'] == 'true':
                    sku['size'] = size['sizeAbbr']
                    sku['sku_id'] = size['skuId']
                    sku['in_stock'] = bool(int(size['quantity']))
                    skus.append(sku)

        return skus

    def add_trail(self, response):
        trail = (response.css('head title::text').get(), response.url)
        return [*response.meta['trail'], trail] if response.meta.get('trail') else [trail]

    def get_sku_requests(self, retialer_sku):
        url = add_or_replace_parameter(self.product_url, 'prodId', retialer_sku)
        return [Request(url=url, callback=self.parse_skus)]

    def get_image_requests(self, retailer_sku):
        url = self.image_url.format(retailer_sku)
        return [Request(url=url, callback=self.parse_image_urls)]

    def get_name(self, response):
        return response.css('h1[itemprop="name"]::text').get()

    def get_sizes(self, response):
        return self.sanitize_list(response.css('.size-button::text').getall())

    def get_product_id(self, response):
        return response.css('input[name="productId"]::attr(value)').get()

    def get_categories(self, response):
        return response.css('.breadcrumb li span[itemprop="name"]::text').getall()[1:-1]

    def get_description(self, response):
        description_css = '.detailsPanel .description::text, .bulletpoint::text'
        return self.sanitize_list(response.css(description_css).getall())

    def get_care(self, response):
        return self.sanitize_list(response.css('.re.subFabricPanel::text').getall())

    def get_image_urls(self, response):
        match = re.search(r'(?<=s7jsonResponse\().*(?=\,\"\"\)\;)', response.text)
        if not match:
            return []

        json_response = json.loads(match.group(0))
        image_url = re.sub(r'LO.*', '', self.image_url)
        image_items = json_response['set']['item']

        if type(image_items) is dict:
            return [f'{image_url}{image_items["i"]["n"]}']

        return [f'{image_url}{url["i"]["n"]}' for url in image_items]

    def sanitize_list(self, inputs):
        return [i.strip() for i in inputs]

    def sanitize_price(self, price):
        return float(''.join(re.findall(r'\d+', price)))

    def get_pricing_details(self, product_details):
        details = {'currency': self.currency}
        details['price'] = self.sanitize_price(product_details['listPrice'])

        if product_details.get('salePrice'):
            details['price'] = self.sanitize_price(product_details['salePrice'])
            details['previous_prices'] = [self.sanitize_price(product_details['listPrice'])]

        return details
