import json
import re
from w3lib.url import add_or_replace_parameter

from scrapy import Request
from scrapy.spiders import Spider
from louandgrey.items import LouandgreyItem


class LouandgreyParser(Spider):
    market = 'US'
    gender = 'women'
    currency = 'USD'
    name = 'louandgreyparser'
    retailer = 'louandgrey-us'
    product_url = 'https://www.louandgrey.com/cws/catalog/product.jsp'
    image_url = 'https://anninc.scene7.com/is/image/LO/{}_IS?req=set,json'

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
        item['pricing_details'] = self.get_pricing_details(response)
        url = add_or_replace_parameter(self.product_url, 'prodId', item['retailer_sku'])

        return Request(url=url, meta={'item': item}, callback=self.parse_skus)

    def parse_skus(self, response):
        item = response.meta['item']
        item['skus'] = self.get_skus(item, json.loads(response.body_as_unicode()))
        url = self.image_url.format(item["retailer_sku"])

        yield Request(url=url, meta={'item': item}, callback=self.parse_image_urls)

    def parse_image_urls(self, response):
        item = response.meta['item']
        clean_response = re.search(r'(?<=s7jsonResponse\().*(?=\,\"\"\)\;)', response.body_as_unicode())

        if clean_response:
            item['image_urls'] = self.get_image_urls(json.loads(clean_response.group(0)))

        yield item

    def add_trail(self, response):
        trail = (response.css('head title::text').get(), response.url)
        return [*response.meta['trail'], trail] if response.meta.get('trail') else [trail]

    def get_name(self, response):
        return response.css('h1[itemprop="name"]::text').get()

    def get_sizes(self, response):
        return self.sanitize_list(response.css('.size-button::text').getall())

    def get_colour_backlog(self, response):
        return response.css('.color-button::attr(href)').getall()

    def get_product_id(self, response):
        return response.css('input[name="productId"]::attr(value)').get()

    def get_categories(self, response):
        return response.css('.breadcrumb li span[itemprop="name"]::text').getall()[1:-1]

    def get_description(self, response):
        description_css = '.detailsPanel .description::text, .bulletpoint::text'
        return self.sanitize_list(response.css(description_css).getall())

    def get_care(self, response):
        return self.sanitize_list(response.css('.re.subFabricPanel::text').getall())

    def get_image_urls(self, json_response):
        image_url = re.sub(r'LO.*', '', self.image_url)
        image_items = json_response['set']['item']

        if type(image_items) is dict:
            return [f'{image_url}{image_items["i"]["n"]}']

        return [f'{image_url}{url["i"]["n"]}' for url in image_items]

    def get_previous_prices(self, response):
        return response.css('del::text').getall()

    def get_skus(self, item, json_response):
        skus = []

        for colour_skus in json_response['products'][0]['skucolors']['colors']:
            sku = item['pricing_details']
            sku['colour'] = colour_skus['colorName']

            for size in colour_skus['skusizes']['sizes']:
                if size['available'] == 'true':
                    sku['size'] = size['sizeAbbr']
                    sku['sku_id'] = size['skuId']
                    sku['in_stock'] = bool(int(size['quantity']))
                    skus.append(sku)

        del item['pricing_details']

        return skus

    def sanitize_list(self, inputs):
        return [i.strip() for i in inputs]

    def sanitize_price(self, price):
        return int(''.join(re.findall(r'\d+', price)))

    def get_pricing_details(self, response):
        price_css = 'meta[itemprop="price"]::attr(content)'

        details = {}
        details['currency'] = self.currency
        details['price'] = self.sanitize_price(response.css(price_css).get())

        previous_prices = response.css('del::text').getall()
        if previous_prices:
            details['previous_prices'] = [self.sanitize_price(p) for p in previous_prices]

        return details
