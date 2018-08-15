import re
import json

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ullapopken.spiders.ullapopken_parser import UllapopkenParser


class UllapopkenCrawler(CrawlSpider, UllapopkenParser):
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }
    name = 'ullapopken'

    start_urls = ["https://www.ullapopken.de/"]
    rules = (Rule(LinkExtractor(restrict_css='.top_level_nav', deny='.*sale.*'),
                  follow=True),
             Rule(LinkExtractor(restrict_css='.toplevel > .nav_content'),
                  callback='parse_category_variables'))

    article_url_t = 'https://www.ullapopken.de/api/res/article/{}'
    items_url_t = 'https://www.ullapopken.de/api/res/category/articles/language/de/' \
                  'size/60/page/{}/category/{}/grouping/{}/filter/_/sort/normal/fs/_'

    def parse_category_variables(self, response):
        category_value = response.css('#paging::attr(data-category)').extract_first()
        grouping_value = response.css('#paging::attr(data-grouping)').extract_first()
        category_request = self.get_category_request(category_value, grouping_value)
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
            category_request = self.get_category_request(category_value, grouping_value, page_number + 1)
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

    def get_category_request(self, category, grouping, page=1):
        url = self.items_url_t.format(page, category, grouping)
        return Request(url=url, callback=self.parse_category)

    @staticmethod
    def get_categories(response):
        return response.css('.active > .nav_content a::text').extract()
