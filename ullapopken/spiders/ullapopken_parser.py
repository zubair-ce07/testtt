import re
import json

from scrapy import Request

from ullapopken.items import UllapopkenItem


class UllapopkenParser:
    genders = [('HERREN', 'Male'),
               ('DAMEN', 'Female')]

    product_url_t = 'https://www.ullapopken.de/produkt/{}/'
    article_url_t = 'https://www.ullapopken.de/api/res/article/{}'
    image_url_t = 'https://up.scene7.com/is/image/UP/{}?fit=constrain,1&wid=1400&hei=2100'

    def parse_color(self, response):
        raw_item = json.loads(response.text)
        item = response.meta.get('item')
        remaining_requests = response.meta.get('remaining_requests')
        item['image_urls'] += self.get_image_urls(raw_item)
        item['skus'] += self.get_skus(raw_item)
        if not remaining_requests:
            return item
        return self.yield_color_request(remaining_requests, item)

    def parse_item(self, response):
        raw_item = json.loads(response.text)
        categories = response.meta.get('categories')
        variants = response.meta.get('variants')
        item = UllapopkenItem()
        item['retailer_sku'] = raw_item['code']
        item['name'] = raw_item['name']
        item['description'] = self.get_description(raw_item)
        item['care'] = self.get_care(raw_item)
        item['brand'] = 'Ullapopken'
        item['url'] = self.get_url(raw_item)
        item['categories'] = categories
        item['gender'] = self.get_gender(categories)
        item['image_urls'] = self.get_image_urls(raw_item)
        item['skus'] = self.get_skus(raw_item)
        if not variants:
            return item
        color_requests = self.get_color_requests(variants)
        return self.yield_color_request(color_requests, item)

    @staticmethod
    def yield_color_request(color_requests, item):
        color_request = color_requests.pop()
        color_request.meta['item'] = item
        color_request.meta['remaining_requests'] = color_requests
        return color_request

    def get_image_urls(self, raw_item):
        picture_codes = self.get_picture_codes(raw_item)
        return [self.image_url_t.format(picture_code) for picture_code in picture_codes]

    @staticmethod
    def get_picture_codes(raw_item):
        raw_pictures = raw_item['pictureMap']
        picture_codes = [raw_pictures['code']]
        return picture_codes + raw_pictures['detailCodes']

    def get_skus(self, raw_item):
        sku_common = dict()
        sku_common['color'] = raw_item['colorLocalized']
        pricing = self.get_pricing(raw_item)
        sku_common['price'] = pricing['price']
        sku_common['old-price'] = pricing['old-price']
        sku_common['currency'] = pricing['currency']
        skus = []
        for raw_sku in raw_item['skuData']:
            sku = sku_common.copy()
            sku['size'] = raw_sku['displaySize']
            if raw_sku['stockLevelStatus'] != 'AVAILABLE':
                sku['is_out_of_stock'] = True
            sku['sku_id'] = raw_sku['skuID']
            skus.append(sku)
        return skus

    def get_pricing(self, raw_item):
        pricing = dict()
        if raw_item['originalPrice']:
            pricing['currency'] = raw_item['originalPrice']['currencyIso']
            pricing['price'] = self.formatted_price(raw_item['originalPrice']['value'])
            pricing['old-price'] = []
        else:
            pricing['currency'] = raw_item['reducedPrice']['currencyIso']
            pricing['price'] = self.formatted_price(raw_item['reducedPrice']['value'])
            pricing['old-price'] = self.formatted_price(raw_item['crossedOutPrice']['value'])
        return pricing

    @staticmethod
    def formatted_price(price):
        return int(float(price) * 100)

    def get_color_requests(self, variants):
        return [Request(url=self.article_url_t.format(variant), callback=self.parse_color)
                for variant in variants]

    @staticmethod
    def get_description(raw_item):
        return re.sub('<[^<]+?>', '', list(raw_item['description'].values())[0])

    @staticmethod
    def get_care(raw_item):
        care_objects = list(raw_item['careInstructions'].values())[0]
        return [care_object['description'] for care_object in care_objects]

    def get_gender(self, categories):
        for gender_token, gender in self.genders:
            if gender_token in categories:
                return gender

    def get_url(self, raw_item):
        return self.product_url_t.format(raw_item['code'])
