# -*- coding: utf-8 -*-
import re
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy import Request
from w3lib.url import url_query_parameter, add_or_replace_parameter

from maurices.maurices_parse_product import MauricesParseProduct


class MauricesSpider(CrawlSpider):
    name = 'maurices_spider'
    start_urls = ['https://www.maurices.com']
    sub_catagory_allow_r = '/p/'
    product_parser = MauricesParseProduct()
    allowed_domains = ['maurices.com', 'mauricesprodatg.scene7.com']
    product_pagination_url_t = 'https://www.maurices.com/maurices/plp/includes' \
        '/plp-filters.jsp?N={sub_catagory_id}&No=0'

    rules = (
        Rule(LinkExtractor(allow=(sub_catagory_allow_r)),callback='parse_subcatagory'),
    )

    def parse_subcatagory(self, response):
        sub_catagory_id = re.findall(r'[0-9]+', response.url)
        url = self.product_pagination_url_t.format(sub_catagory_id=sub_catagory_id[0])

        yield Request(url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        yield from self.product_requests(response)

        next_page_url = json.loads(response.body).get('nextPageUrl')
        if next_page_url:
            product_count = url_query_parameter(next_page_url, 'No')
            url = add_or_replace_parameter(response.url, 'No', product_count)

            yield Request(url, callback=self.parse_pagination,)

    def product_requests(self, response):
        product_urls = self.product_urls(response)
        requests = []

        for product_url in product_urls:
            requests.append(Request(response.urljoin(product_url),
                                    callback=self.product_parser.parse_product))
        return requests

    def product_urls(self, response):
        raw_page = json.loads(response.body).get('product_grid').get('html_content')
        css = '.mar-prd-item-image-container::attr(href)'
        return Selector(text=raw_page).css(css).extract()

