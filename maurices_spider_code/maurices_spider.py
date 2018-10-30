# -*- coding: utf-8 -*-
import re
import json
import w3lib

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from maurices.maurices_parse_product import MauricesParseProduct


class MauricesSpider(CrawlSpider):
    name = 'maurices_spider'
    allowed_domains = ['maurices.com', 'mauricesprodatg.scene7.com']
    start_urls = ['https://www.maurices.com']
    product_pagination_url_t = 'https://www.maurices.com/maurices/plp/includes' \
        '/plp-filters.jsp?N={sub_catagory_id}&No=0'
    sub_catagory_allow_r = '/p/'
    product_parser = MauricesParseProduct()

    rules = (Rule(LinkExtractor(allow=(sub_catagory_allow_r)),
                  callback='parse_subcatagory'),)

    def parse_subcatagory(self, response):
        sub_catagory_id_re = re.compile(r'[0-9]+')
        sub_catagory_id = sub_catagory_id_re.findall(response.url)
        url = self.product_pagination_url_t.format(
            sub_catagory_id=sub_catagory_id[0])
        yield scrapy.Request(url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        response_json = json.loads(response.body)
        html_response = response_json.get('product_grid')
        html_response = html_response.get('html_content')
        product_requests = self.product_requests(html_response, response)
        for product_request in product_requests:
            yield product_request
        next_page_url = response_json.get('nextPageUrl')
        if next_page_url:
            product_count = w3lib.url.url_query_parameter(next_page_url, 'No')
            url = w3lib.url.add_or_replace_parameter(
                response.url, 'No', product_count)
            yield scrapy.Request(url, callback=self.parse_pagination,)

    def product_requests(self, html_response, response):
        product_url_css = '.mar-prd-item-image-container::attr(href)'
        product_urls = Selector(text=html_response).css(
            product_url_css).extract()
        requests = []
        for product_url in product_urls:
            requests.append(scrapy.Request(response.urljoin(product_url),
                                           callback=self.product_parser.parse_product))
        return requests

