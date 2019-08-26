# -*- coding: utf-8 -*-
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
import w3lib.url

from .americangolf_parser import AmericangolfParser

class AmericangolfSpider(CrawlSpider):
    name = 'americangolf'
    allowed_domains = ['americangolf.co.uk']
    start_urls = ['http://americangolf.co.uk/']
    product_parser = AmericangolfParser()
    header_css = '.header-navigation-left'

    rules = (
        Rule(LinkExtractor(
            restrict_css=(f"{header_css} a.a-level-2, {header_css} a.a-level-1, {header_css} .fly-content")),
            callback='parse_category'),
    )

    def parse_category(self, response):
        yield from self.product_requests(response)

        infinite_scroll = response.css('.search-result-items::attr(data-infinitescroll)').get()
        if infinite_scroll:
            raw_pagination = json.loads(infinite_scroll)
            products_in_page = raw_pagination['pageSize']
            total_products = raw_pagination['productCount']
            if total_products > products_in_page:
                url = w3lib.url.add_or_replace_parameter(response.url, 'sz', total_products)
                url = w3lib.url.add_or_replace_parameter(url, 'start', products_in_page)
                yield Request(url, callback=self.product_requests)

    def product_requests(self, response):
        products = response.css('.search-result-items .product-name a.productlink::attr(href)').getall()
        return [Request(url, callback=self.product_parser.parse_product) for url in products]
