import json

import scrapy
from scrapy.item import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import SelectorList
from scrapy.spiders import CrawlSpider, Rule, Request


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
    default_size = 'One_Size'

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
    product_css = '.item .pic-detail'
    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_pagination(self, response):
        total_items = int(response.css('script::text').re_first(r'var totalItem  = \"(.+)\"'))
        page_size = int(response.css('script::text').re_first(r'var itemPerPage = \"(.+)\"'))
        total_pages = total_items//page_size + 1

        category_id = clean(response.css('.f-filter ::attr(data-id)'))[0]

        for page_number in range(0, total_pages):
            url = self.pagination_url_t.format(page_number, category_id)
            yield Request(url=url, callback=self.parse)

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
        item['image_urls'] = self.extract_image_urls(response)
        item['skus'] = self.extract_skus(response)
        item['requests_queue'] = self.construct_sku_requests(response)

        return self.get_item_or_next_request(item)

    def parse_colour(self, response):
        item = response.meta['item']
        item['image_urls'] += self.extract_image_urls(response)
        item['skus'] += self.extract_skus(response)

        return self.get_item_or_next_request(item)

    def extract_item_name(self, response):
        return clean(response.css('.gr_title .head ::text'))[0]

    def extract_brand_name(self, response):
        return self.default_brand

    def extract_retailer_sku(self, response):
        return clean(response.css('.gr_title .head em::text'))[0]

    def extract_gender(self, response):
        for gender in self.raw_category(response):
            if gender.lower() in self.gender_terms:
                return gender.lower()

        return self.default_gender

    def extract_care(self, response):
        raw_cares = self.raw_description(response)
        return [care for care in raw_cares if any(care_t in care for care_t in self.care_terms)]

    def extract_description(self, response):
        raw_description = self.raw_description(response)
        return [desc for desc in raw_description if all(c not in desc for c in self.care_terms)]

    def raw_description(self, response):
        css = '.accord-content p:nth-child(1)::text, .accord-content span::text'
        raw_description = clean(response.css(css))

        return [desc for sublist in raw_description for desc in sublist.split('.') if desc]

    def raw_category(self, response):
        return clean(response.css('.crumb-list a::text'))

    def extract_category(self, response):
        return self.raw_category(response)

    def extract_image_urls(self, response):
        return clean(response.css('.show-scroll-list ::attr(src)'))

    def extract_colour(self, response):
        raw_color = clean(response.css('.pro-color .head span::text'))
        if raw_color:
            return raw_color[0]

        return None

    def extract_previous_prices(self, response):
        return response.css('.past ::text').re(r'(\d+\.\d+)')

    def extract_current_price(self, response):
        return response.css('.now .markdown::text, .now .number::text').re_first(r'(\d+\.\d+)')

    def extract_currency(self, response):
        raw_currency = json.loads(response.css('script::text').re_first(r'utag_data = (.*);'))
        return raw_currency.get('site_currency')

    def get_item_or_next_request(self, item):
        if not item['requests_queue']:
            del item['requests_queue']
            return item

        request = item['requests_queue'].pop()
        request.meta['item'] = item

        return request

    def construct_sku_requests(self, response):
        sku_urls = clean(response.css('.pro-color ::attr(href)'))
        return [response.follow(url=url, callback=self.parse_colour) for url in sku_urls]

    def extract_skus(self, response):
        skus = []
        colour = self.extract_colour(response)
        common_sku = {
            'price': self.extract_current_price(response),
            'currency': self.extract_currency(response),
            'previous_prices': self.extract_previous_prices(response)
        }

        if colour:
            common_sku['colour'] = colour

        for size in clean(response.css('.pro-size-con [data-title="IN STOCK"]::text')) or [self.default_size]:
            sku = common_sku.copy()
            sku['size'] = size
            sku['sku_id'] = f'{colour}_{size}' if colour else size

            skus.append(sku)

        return skus


def clean(raw_item):
    if isinstance(raw_item, str):
        return raw_item.strip()
    elif isinstance(raw_item, SelectorList):
        return [r.strip() for r in raw_item.getall() if r.strip()]

    return [r.strip() for r in raw_item if r.strip()]
