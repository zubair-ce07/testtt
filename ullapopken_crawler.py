import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request

from ullapopken_parser import UllaPopKenParser


class UllaPopKenCrawler(CrawlSpider, UllaPopKenParser):
    name = 'ullapopken'
    allowed_domains = ['ullapopken.com']
    start_urls = ['https://www.ullapopken.com/']
    default_brand = 'Ullapopken'

    category_url_t = 'https://www.ullapopken.com/api/res/category/articles/language/en/' \
                     'size/60/page/1/category/{}/grouping/{}/filter/_/sort/normal/fs/_'
    all_items_url_t = 'https://www.ullapopken.com/api/res/category/articles/language/en/' \
                      'size/{}/page/1/category/{}/grouping/{}/filter/_/sort/normal/fs/_'

    variant_url_t = 'https://www.ullapopken.com/api/res/model/{}/variants'

    category_css = '.first-row'
    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse_category_parameters'),
    )

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
            item_request = Request(self.variant_url_t.format(item_code), callback=self.parse_item)

            item_request.meta['category'] = response.meta['category']
            item_request.meta['url'] = data['url']
            item_request.meta['retailer_sku'] = item_code

            yield item_request

