import json
import math

import scrapy
from scrapy import Request
from scrapy.item import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


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


class JeanWestSpider(CrawlSpider):
    name = 'jeans_west'
    allowed_domains = ['jeanswest.com.au']
    start_urls = ['https://www.jeanswest.com.au/en-au/']

    default_brand = 'JeansWest'
    default_gender = 'unisex'
    default_size = 'M'

    gender_terms = [
        'women',
        'men',
    ]
    care_terms = [
        'Composition',
        'Material',
        'Made from',
        'Madefrom'
    ]

    pagination_url_t = 'https://www.jeanswest.com.au/en-au/category_filter?p={}&category_id={}'
    category_css = '.list-li:not(.head)'
    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse_pagination'),
    )

    def parse_pagination(self, response):
        pagination_pages = self.get_pagination_pages(response)
        category_id = response.css('.f-filter ::attr(data-id)').get()

        for page_number in range(0, pagination_pages):
            url = self.pagination_url_t.format(page_number, category_id)
            yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        item_links = response.css('.item .pic-detail ::attr(href)').getall()
        yield from [Request(item_link, callback=self.parse_item) for item_link in item_links]

    def parse_item(self, response):
        item = Product()
        item['url'] = response.url
        item['name'] = self.extract_item_name(response)
        item['brand'] = self.extract_brand_name(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        item['requests_queue'] = self.construct_sku_requests(response)
        item['skus'] = []
        item['image_urls'] = []

        if not self.has_color_skus(response):
            item['image_urls'] = self.extract_image_urls(response)
            item['skus'] = self.extract_skus(response)
            del item['requests_queue']
            return item

        return self.get_item_or_parse_request(item)

    def extract_item_name(self, response):
        return response.css('.gr_title .head ::text').get().strip()

    def extract_brand_name(self, response):
        return self.default_brand

    def extract_retailer_sku(self, response):
        return response.css('.gr_title .head em::text').get()

    def extract_gender(self, response):
        raw_genders = response.css('.crumb-list a::text').getall()

        for gender in clean(raw_genders):
            if gender.lower() in self.gender_terms:
                return gender.lower()

        return self.default_gender

    def extract_care(self, response):
        css = '.accord-content p:nth-child(1)::text, .accord-content span::text'
        raw_cares = response.css(css).getall()

        return [care for care in raw_cares if any(care_t in care for care_t in self.care_terms)]

    def extract_category(self, response):
        return response.css('.crumb-list a::text').getall()

    def extract_description(self, response):
        css = '.accord-content p:nth-child(1)::text, .accord-content span::text'
        raw_description = response.css(css).getall()

        return [desc for sublist in clean(raw_description) for desc in sublist.split('.') if desc]

    def extract_image_urls(self, response):
        return response.css('.show-scroll-list ::attr(src)').getall()

    def extract_colour(self, response):
        return response.css('.pro-color .head span::text').get()

    def extract_previous_prices(self, response):
        return response.css('.past ::text').re(r'(\d+\.\d+)')

    def extract_current_price(self, response):
        return response.css('.now .markdown::text, .now .number::text').re_first(r'(\d+\.\d+)')

    def extract_currency(self, response):
        raw_currency = json.loads(response.css('script::text').re_first(r'utag_data = (.*);'))
        return raw_currency.get('site_currency')

    def has_color_skus(self, response):
        return response.css('.pro-color ::attr(href)').getall()

    def get_item_or_parse_request(self, item):
        if not item['requests_queue']:
            del item['requests_queue']
            return item

        request = item['requests_queue'].pop()
        request.meta['item'] = item

        return request

    def construct_sku_requests(self, response):
        sku_urls = response.css('.pro-color ::attr(href)').getall()
        return [response.follow(url=url, callback=self.parse_sku) for url in sku_urls]

    def parse_sku(self, response):
        item = response.meta['item']
        item['image_urls'].extend(self.extract_image_urls(response))

        if self.extract_skus(response):
            item['skus'].extend(self.extract_skus(response))

        return self.get_item_or_parse_request(item)

    def extract_skus(self, response):
        skus = []
        colour = self.extract_colour(response)
        item_sizes = response.css('.pro-size-con [data-title="IN STOCK"]::text').getall()
        common_sku = {
            'price': self.extract_current_price(response),
            'currency': self.extract_currency(response),
            'previous_prices': self.extract_previous_prices(response)
        }

        if colour:
            common_sku['colour'] = colour

        if not item_sizes:
            common_sku['sku_id'] = f'{self.default_size}'
            common_sku['size'] = self.default_size
            return skus.append(common_sku)

        for item_size in item_sizes:
            sku = common_sku.copy()
            sku['size'] = item_size
            if colour:
                sku['sku_id'] = f'{colour}_{item_size}'
            else:
                sku['sku_id'] = f'{item_size}'

            skus.append(sku)

        return skus

    def get_pagination_pages(self, response):
        total_items = int(response.css('script::text').re_first(r'var totalItem  = \"(.+)\"'))
        items_per_page = int(response.css('script::text').re_first(r'var itemPerPage = \"(.+)\"'))

        return math.ceil(total_items / items_per_page)


def clean(raw_list):
    return [list_item.strip() for list_item in raw_list if list_item.strip()]
