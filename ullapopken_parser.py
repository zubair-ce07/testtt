import json

import scrapy
from scrapy.item import Item
from scrapy.selector import SelectorList
from scrapy.spiders import Request


class Product(Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()
    requests_queue = scrapy.Field()


class UllaPopKenParser:
    default_brand = 'Ullapopken'

    default_gender = 'unisex'
    gender_terms = [
        'women',
        'men',
    ]

    sku_url_t = 'https://www.ullapopken.com/api/res/article/{}'

    def parse_item(self, response):
        item = Product()
        item['url'] = response.meta['url']
        item['retailer_sku'] = response.meta['retailer_sku']
        item['category'] = response.meta['category']
        item['brand'] = self.extract_brand_name(response)
        item['gender'] = self.extract_gender(response.meta['category'])
        item['requests_queue'] = self.construct_item_requests(response)
        item['skus'] = []
        item['image_urls'] = []

        return self.get_item_or_parse_request(item)

    def parse_colour_dependent_values(self, response):
        item = response.meta['item']
        raw_item = json.loads(response.text)
        item['name'] = self.extract_item_name(raw_item)
        item['care'] = self.extract_care(raw_item)
        item['description'] = self.extract_description(raw_item)
        item['image_urls'] += self.extract_image_urls(raw_item)
        item['skus'] += self.extract_skus(raw_item)

        return self.get_item_or_parse_request(item)

    def extract_skus(self, raw_item):
        skus = []
        common_sku = {
            'colour': raw_item['colorLocalized']
        }

        for item in raw_item['skuData']:
            sku = common_sku.copy()
            sku['size'] = item['displaySize']
            sku['sku_id'] = item['skuID']
            sku.update(self.extract_pricing(item))

            skus.append(sku)

        return skus

    def construct_item_requests(self, response):
        response_json = json.loads(response.text)
        colour_codes = [data['articleCode'] for data in response_json]

        return [Request(url=self.sku_url_t.format(c), callback=self.parse_colour_dependent_values)
                for c in colour_codes]

    def get_item_or_parse_request(self, item):
        if not item['requests_queue']:
            del item['requests_queue']
            return item

        request = item['requests_queue'].pop()
        request.meta['item'] = item

        return request

    def extract_pricing(self, raw_price):
        pricing = {}
        price = raw_price['reducedPrice'] or raw_price['originalPrice']
        pricing['currency'] = price['currencyIso']
        pricing['previous_prices'] = [raw_price['crossedOutPrice']['value']] \
            if raw_price['crossedOutPrice'] else []

        pricing['price'] = price['value']

        return pricing

    def extract_item_name(self, raw_item):
        return raw_item['name']

    def extract_brand_name(self, response):
        return self.default_brand

    def extract_gender(self, raw_genders):

        for gender in raw_genders:
            if gender.lower() in self.gender_terms:
                return gender.lower()

        return self.default_gender

    def extract_category(self, response):
        return clean(response.css('.active > .nav_content ::text'))

    def extract_image_urls(self, raw_item):
        return [image_data['url'] for image_data in raw_item['imageDataList']]

    def extract_care(self, raw_item):
        raw_care = raw_item['careInstructions'][raw_item['code']]
        return [care['description'] for care in raw_care]

    def extract_description(self, raw_item):
        return clean(raw_item['description'][raw_item['code']])


def clean(raw_item):
    if isinstance(raw_item, str):
        return raw_item.strip()
    elif isinstance(raw_item, SelectorList):
        return [r.strip() for r in raw_item.getall() if r.strip()]

    return [r.strip() for r in raw_item if r.strip()]
