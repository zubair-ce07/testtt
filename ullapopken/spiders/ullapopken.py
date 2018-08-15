import re
import json

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ullapopken.items import UllapopkenItem


class Ullapopken(CrawlSpider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1}
    name = 'ullapopken'

    start_urls = ["https://www.ullapopken.de/"]
    rules = (Rule(LinkExtractor(restrict_css='.top_level_nav', deny='.*sale.*'),
                  follow=True),
             Rule(LinkExtractor(restrict_css='.toplevel > .nav_content'),
                  callback='parse_category_variables'))

    genders = [('HERREN', 'Male'),
               ('DAMEN', 'Female')]

    product_url_t = 'https://www.ullapopken.de/produkt/{}/'
    article_url_t = 'https://www.ullapopken.de/api/res/article/{}'
    items_url_t = 'https://www.ullapopken.de/api/res/category/articles/language/de/' \
                  'size/60/page/{}/category/{}/grouping/{}/filter/_/sort/normal/fs/_'
    image_url_t = 'https://up.scene7.com/is/image/UP/{}?fit=constrain,1&wid=1400&hei=2100'

    def parse_category_variables(self, response):
        category_value = response.css('#paging::attr(data-category)').extract_first()
        grouping_value = response.css('#paging::attr(data-grouping)').extract_first()
        category_request = self.make_category_request(category_value, grouping_value)
        category_request.meta['categories'] = self.get_categories(response)
        return category_request

    def parse_category(self, response):
        categories = response.meta.get('categories')
        response_json = json.loads(response.text)
        items = response_json['results']
        for item_request in self.get_item_requests(items, categories):
            yield item_request
        return self.get_pagination_requests(response_json['pagination'], response.url, categories)

    def get_pagination_requests(self, pagination, url, categories):
        if pagination['currentPage'] != 0:
            return

        category_value = re.findall('category.*category/(.+)/grouping', url)[0]
        grouping_value = re.findall('grouping/(.+)/filter', url)[0]

        for page_number in range(1, pagination['numberOfPages']):
            category_request = self.make_category_request(category_value, grouping_value, page_number+1)
            category_request.meta['categories'] = categories
            yield category_request

    def get_item_requests(self, items, categories):
        item_requests = []
        for item in items:
            item_request = Request(url=self.article_url_t.format(item['code']), callback=self.parse_item)
            item_request.meta['categories'] = categories
            item_request.meta['variants'] = self.get_variants_codes(item)
            item_requests.append(item_request)
        return item_requests

    @staticmethod
    def get_variants_codes(item):
        variants = item['variantsArticlenumbers']
        variants.remove(item['code'])
        return variants

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

    def make_category_request(self, category, grouping, page=1):
        url = self.items_url_t.format(page, category, grouping)
        return Request(url=url, callback=self.parse_category)

    @staticmethod
    def get_categories(response):
        return response.css('.active > .nav_content a::text').extract()
