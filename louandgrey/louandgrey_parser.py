import json
from re import sub
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
        item['retailer_sku'] = self.get_product_id(response)
        item['description'] = self.get_description(response)
        item['category'] = self.get_categories(response)
        item['pricing_details'] = self.get_pricing_details(response)

        return Request(url=add_or_replace_parameter(self.product_url, 'prodId', item['retailer_sku']),
                       meta={'item': item}, callback=self.parse_skus)

    def parse_skus(self, response):
        item = response.meta['item']
        item['skus'] = self.get_skus(item, json.loads(response.body_as_unicode()))
        yield Request(url=self.image_url.format(item["retailer_sku"]), meta={'item': item},
                      callback=self.parse_image_urls)

    def parse_image_urls(self, response):
        item = response.meta['item']
        response_body = response.body_as_unicode()
        response_body = sub(r'\/\*jsonp\*\/s7jsonResponse\(', '', response_body)
        response_body = sub(r',""\);', '', response_body)
        item['image_urls'] = self.get_image_urls(json.loads(response_body))
        yield item

    def add_trail(self, response):
        trail = (response.css('head title::text').get(), response.url)
        return [*response.meta['trail'], trail] if response.meta.get('trail') else [trail]

    def get_in_stock(self, response):
        in_stock = response.css('.in-stock-msg::text').get()
        return int(sub(r'\sitem\sleft', '', in_stock)) if in_stock else 0

    def get_currency(self, response):
        return response.css('input[name="currency"]::attr(value)')

    def get_name(self, response):
        return response.css('h1[itemprop="name"]::text').get()

    def get_sizes(self, response):
        return [s.strip() for s in response.css('.size-button::text').getall()]

    def get_colour_backlog(self, response):
        return response.css('.color-button::attr(href)').getall()

    def get_product_id(self, response):
        return response.url.split('/')[-1]

    def get_categories(self, response):
        return response.css('.breadcrumb li span[itemprop="name"]::text').getall()[1:-1]

    def get_description(self, response):
        descriptions = response.css('.detailsPanel .description::text, .bulletpoint::text').getall()
        return [description.strip() for description in descriptions]

    def get_care(self, response):
        return [care.strip() for care in response.css('.subFabricPanel::text').getall()]

    def get_image_urls(self, json_response):
        image_url = sub(r'LO.*', '', self.image_url)
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
                    sku['in_stock'] = size['quantity']
                    skus.append(sku)
        del item['pricing_details']
        return skus

    def get_pricing_details(self, response):
        details = {}
        details['currency'] = self.currency
        details['price'] = int(response.css('meta[itemprop="price"]::attr(content)').get().replace('.', ''))
        previous_prices = response.css('del::text').getall()
        if previous_prices:
            details['previous_prices'] = [int(p[1:].replace('.', '')) for p in previous_prices]
        return details
