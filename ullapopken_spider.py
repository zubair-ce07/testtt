import json

import scrapy
from scrapy.item import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import SelectorList
from scrapy.spiders import CrawlSpider, Rule, Request, Spider


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


class UllaPopKenParser(Spider):
    name = "ullapopken_parser"
    default_brand = 'Ullapopken'

    default_gender = 'unisex'
    gender_terms = [
        'women',
        'men',
    ]

    sku_url_t = 'https://www.ullapopken.com/api/res/article/{}'

    def parse(self, response):
        item = Product()
        item['url'] = response.meta['url']
        item['name'] = response.meta['name']
        item['retailer_sku'] = response.meta['retailer_sku']
        item['category'] = response.meta['category']
        item['brand'] = self.extract_brand_name(response)
        item['gender'] = self.extract_gender(response.meta['category'])
        item['requests_queue'] = self.construct_colour_requests(response)
        item['skus'] = []
        item['image_urls'] = []
        item['care'] = []
        item['description'] = []

        return self.get_item_or_parse_request(item)

    def parse_colour(self, response):
        item = response.meta['item']
        raw_item = json.loads(response.text)

        item['care'] += self.extract_care(raw_item)
        item['description'] += self.extract_description(raw_item)
        item['image_urls'] += self.extract_image_urls(raw_item)
        item['skus'] += self.extract_skus(raw_item)

        return self.get_item_or_parse_request(item)

    def extract_skus(self, raw_item):
        skus = []
        common_sku = {
            'colour': raw_item['colorLocalized']
        }

        for raw_sku in raw_item['skuData']:
            sku = common_sku.copy()
            sku['size'] = raw_sku['displaySize']
            sku['sku_id'] = raw_sku['skuID']
            sku.update(self.extract_pricing(raw_sku))

            skus.append(sku)

        return skus

    def construct_colour_requests(self, response):
        response_json = json.loads(response.text)

        return [Request(url=self.sku_url_t.format(c['articleCode']), callback=self.parse_colour)
                for c in response_json]

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
        pricing['price'] = price['value']

        if raw_price.get('crossedOutPrice'):
            pricing['previous_prices'] = [raw_price['crossedOutPrice']['value']]

        return pricing

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
        return clean([raw_item['description'][raw_item['code']]])


def clean(raw_item):
    if isinstance(raw_item, str):
        return raw_item.strip()
    elif isinstance(raw_item, SelectorList):
        return [r.strip() for r in raw_item.getall() if r.strip()]

    return [r.strip() for r in raw_item if r.strip()]


class UllaPopKenCrawler(CrawlSpider, UllaPopKenParser):
    name = 'ullapopken'
    allowed_domains = ['ullapopken.com']
    start_urls = ['https://www.ullapopken.com/']

    category_url_t = 'https://www.ullapopken.com/api/res/category/articles/language/en/' \
                     'size/60/page/1/category/{}/grouping/{}/filter/_/sort/normal/fs/_'
    all_items_url_t = 'https://www.ullapopken.com/api/res/category/articles/language/en/' \
                      'size/{}/page/1/category/{}/grouping/{}/filter/_/sort/normal/fs/_'

    variant_url_t = 'https://www.ullapopken.com/api/res/model/{}/variants'

    category_css = '.first-row'
    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse_category_parameters'),
    )

    parser = UllaPopKenParser()

    def parse_category_parameters(self, response):
        category = response.css('#paging::attr(data-category)').get()
        grouping = response.css('#paging::attr(data-grouping)').get()
        pagination_url = self.category_url_t.format(category, grouping)

        pagination_request = Request(url=pagination_url, callback=self.parse_pagination)
        pagination_request.meta['category'] = category
        pagination_request.meta['grouping'] = grouping
        pagination_request.meta['item_category'] = self.extract_category(response)

        yield pagination_request

    def parse_pagination(self, response):
        category = response.meta['category']
        grouping = response.meta['grouping']
        response_json = json.loads(response.text)

        total_items = response_json['pagination']['totalNumberOfResults']
        category_url = self.all_items_url_t.format(total_items, category, grouping)

        pagination_request = Request(url=category_url, callback=self.parse_category)
        pagination_request.meta['category'] = response.meta['item_category']

        yield pagination_request

    def parse_category(self, response):
        response_json = json.loads(response.text)

        for data in response_json['results']:
            item_code = data['masterArticlenumber']
            item_request = Request(self.variant_url_t.format(item_code), callback=self.parser.parse)

            item_request.meta['category'] = response.meta['category']
            item_request.meta['url'] = data['url']
            item_request.meta['name'] = data['name']
            item_request.meta['retailer_sku'] = item_code

            yield item_request
