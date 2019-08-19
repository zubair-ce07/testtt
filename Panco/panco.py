# -*- coding: utf-8 -*-
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import w3lib.url

from .panco_parser import PancoParserSpider

class PancoCrawlerSpider(CrawlSpider):
    name = 'panco_crawler'
    allowed_domains = ['panco.com.tr']
    start_urls = ['https://panco.com.tr/']
    product_parser = PancoParserSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=('.js-categories-carousel')), callback='parse_category'),
    )

    def parse_category(self, response):
        next_page = response.css(".paginate-bottom a.js-pagination-next::attr(href)").get()
        page_num = re.findall("\\d+", next_page)
        if page_num:
            url = w3lib.url.add_or_replace_parameter(response.request.url, 'page', page_num[0])
            yield response.follow(url, self.parse_category)

        products = response.css(".product-item-info a::attr(href)").getall()
        for product in products:
            yield response.follow(product, self.product_parser.parse_product)
