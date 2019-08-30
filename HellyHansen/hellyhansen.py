# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import w3lib.url

from .hellyhansen_parser import HellyhansenParser

class HellyhansenSpider(CrawlSpider):
    name = 'hellyhansen'
    allowed_domains = ['hellyhansen.com']
    start_urls = ['http://hellyhansen.com/en_gb/']
    product_parser = HellyhansenParser()

    rules = (
        Rule(LinkExtractor(
            restrict_css=('.v-navigation__inner.v-navigation__inner--level2'),
            allow=[r'/en_gb/']), callback='parse_category'),
    )

    def parse_category(self, response):
        yield from self.parse_product_requests(response)

        data_pages = response.css(".b-toolbar.b-toolbar--bottom .infinite-scrolling::attr(data-page-count)").get(default='1')
        for page_num in range(2, int(data_pages)+1):
            url = w3lib.url.add_or_replace_parameter(response.url, 'p', page_num)
            request = Request(url, callback=self.parse_product_requests)
            yield request

    def parse_product_requests(self, response):
        products = response.css(".b-products__item.item.product.product-item a::attr(href)").getall()
        return [Request(url, callback=self.product_parser.parse) for url in products]
