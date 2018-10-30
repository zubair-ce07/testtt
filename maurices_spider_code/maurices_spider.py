# -*- coding: utf-8 -*-
import re
import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from maurices.maurices_parse_product import MauricesParseProduct


class MauricesSpider(CrawlSpider):
    name = 'maurices_spider'
    product_pagination_url_t = 'https://www.maurices.com/maurices/plp/includes/plp-filters.jsp?N={sub_catagory_id}&No=0'
    allowed_domains = ['maurices.com', 'mauricesprodatg.scene7.com']
    start_urls = ['https://www.maurices.com']
    sub_catagory_allow_r = '/p/'

    rules = (Rule(LinkExtractor(allow=(sub_catagory_allow_r)),
                  callback='parse_product_subcatagory'),)

    def parse_product_subcatagory(self, response):
        sub_catagory_id_re = re.compile(r'[0-9]+')
        sub_catagory_id = sub_catagory_id_re.search(response.url).group()
        url = self.product_pagination_url_t.format(
            sub_catagory_id=sub_catagory_id)
        yield scrapy.Request(url, callback=self.parse_pagination, meta={'product_urls': []})

    def parse_pagination(self, response):
        product_urls = response.meta.get('product_urls')
        response_json = json.loads(response.body)
        html_response = response_json.get('product_grid')
        html_response = html_response.get('html_content')
        product_url_css = '.mar-prd-item-image-container::attr(href)'
        product_urls.extend(Selector(text=html_response).css(
            product_url_css).extract())
        next_page_url = response_json.get('nextPageUrl')
        if next_page_url:
            url = response.url
            url = url[:url.find('No=')+3]
            url = url + re.search('No=(.+?)&', next_page_url).group(1)
            yield scrapy.Request(url, callback=self.parse_pagination,
                                 meta={'product_urls': product_urls})
        else:
            product_parser = MauricesParseProduct()
            for product_url in product_urls:
                yield scrapy.Request(response.urljoin(product_url),
                                     callback=product_parser.parse_product)

