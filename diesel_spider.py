import json
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import DieselItem


class DieselParser:

    def parse_details(self, response):
        item = DieselItem()

        item['retailer_sku'] = self.extract_retailor_sku(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['brand'] = self.extract_brand()
        item['url'] = self.extract_url(response)
        item['name'] = self.extract_name(response)
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['image_urls'] = self.extract_img_urls(response)
        item['skus'] = self.extract_skus(response)

        yield item

    def extract_retailor_sku(self, response):
        return response.css('script::text').re_first("\['product_sku'\] = '([^\n\r]*)'")

    def extract_gender(self, response):
        return re.search('men|women', response.meta['trail']).group()

    def extract_category(self, response):
        return response.meta['trail'].replace('https://www.diesel.cn/', '').split('/')

    def extract_brand(self):
        return 'Diesel'

    def extract_url(self, response):
        return response.url

    def extract_name(self, response):
        return response.css('.name ::text').get()

    def extract_description(self, response):
        return self.clean(response.css('.tab-detail::text').getall())

    def extract_care(self, response):
        return self.clean(response.css('.tab-detail p::text').getall())

    def extract_common_sku(self, response):
        sku = {'currency': 'CNY'}
        sku['price'] = self.clean(response.css('.price_default::text').get())
        sku['previous_price'] = []
        return sku

    def extract_img_urls(self, response):
        colors = json.loads(response.css('script::text').re_first('gallery = ([^\n\r]*);'))
        return [color['images'] for color in colors]

    def extract_skus(self, response):
        common_sku = self.extract_common_sku(response)
        colors = json.loads(response.css('script::text').re_first('spConfig = ([^\n\r]*);'))[0]['options']
        sizes = json.loads(response.css('script::text').re_first('spConfig = ([^\n\r]*);'))[1]['options']
        skus = []
        for color in colors:
            for size in sizes:
                sku = common_sku.copy()
                sku['colour'] = color['label']
                sku['size'] = size['label']
                sku['out_of_stock'] = not any(c in size['products'] for c in color['products'])
                sku['sku_id'] = f'{sku["colour"]}_{sku["size"]}'
                skus.append(sku)

        return skus

    def clean(self, list_to_strip):
        if isinstance(list_to_strip, str):
            return list_to_strip.strip()
        return [str_to_strip.strip() for str_to_strip in list_to_strip if str_to_strip.strip()]


class DieselSpider(CrawlSpider):
    name = 'dieselSpider'
    allowed_domains = ['diesel.cn']
    start_urls = [
        'https://www.diesel.cn/',
    ]
    listing_css = ['.item .list']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_pagination'),
    )
    product_parser = DieselParser()
    pagination_template = 'https://www.diesel.cn/api/rest/products?limit={}&page={}&category_id={}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def parse_pagination(self, response):
        category_id = response.css('script::text').re_first("category_id = '([^\n\r]*)';")
        total_pages = int(response.css('script::text').re_first("total_page = ([^\n\r]*);"))
        limit = response.css('script::text').re_first("limit = ([^\n\r]*);")
        trail = response.url
        for page in range(1, total_pages):
            page_url = self.pagination_template.format(limit, page, category_id)
            yield response.follow(page_url, callback=self.parse_category, meta={'trail': trail},
                                  headers=self.headers)

    def parse_category(self, response):
        products = json.loads(response.text)['data']['products']
        trail = response.meta['trail']
        for product in products:
            yield response.follow(product['url'], self.product_parser.parse_details, meta={'trail': trail})


class DieselItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
