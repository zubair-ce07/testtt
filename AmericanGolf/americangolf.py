# -*- coding: utf-8 -*-
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
from scrapy import Request
import w3lib.url

from .americangolf_parser import AmericangolfParser

class AmericangolfSpider(CrawlSpider):
    name = 'americangolf'
    allowed_domains = ['americangolf.co.uk']
    start_urls = ['http://americangolf.co.uk/']
    product_parser = AmericangolfParser()
    HN = '.header-navigation-left'

    rules = (
        Rule(LinkExtractor(
            restrict_css=(f"{HN} a.a-level-2, {HN} a.a-level-1, {HN} .fly-content")),
            callback='parse_category'),
    )

    def parse_category(self, response):
        yield from self.product_requests(response)

        infinite_scroll = response.css('.search-result-items::attr(data-infinitescroll)').get()
        if infinite_scroll:
            pagging = json.loads(infinite_scroll)
            page_size = pagging['pageSize']
            product_count = pagging['productCount']
            if product_count > page_size:
                url = w3lib.url.add_or_replace_parameter(response.request.url, 'sz', product_count)
                url = w3lib.url.add_or_replace_parameter(url, 'start', page_size)
                yield Request(url, callback=self.product_requests)

    def product_requests(self, response):
        products = response.css('.search-result-items .product-name a.productlink::attr(href)').getall()
        return [Request(url, callback=self.product_parser.parse_product) for url in products]
