# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.Request import Request


class HarrodsSpider(CrawlSpider):
    name = 'harrods'
    allowed_domains = ['harrods.com']
    start_urls = ['http://harrods.com/']
    rules = (
            Rule(LinkExtractor(
                deny=('/designers/', '/style-notes'),
                restrict_css='.nav_list'),
                callback='parse_listing',),
            )

    def parse_listing(self, response):
        for url in self.get_product_urls(response):
            yield Request(url=url, callback=self.parse_product)
        for next_page in self.get_next_pages:
            yield Request(url=url, callback=self.parse_listing)

    def parse_product(self, response):
        pass

    def get_product_urls(self, response):
        return response.css(
            ".product-grid_list .product-card_link::attr(href)").extract()

    def get_next_pages(self, response):
        urls = response.css(".control_paging-list a::attr(href)").extract()
        urls = list(set(urls))
        return [response.urljoin(url) for url in urls]

    def get_currency_control_url(self, response):
        # find default color
        product_code = response.css(
            'input[name="ProductCode"]::attr(value)').extract()
        product_template = response.css(
            'input[name="PdpTemplateType"]::attr(value)').extract()
        product_bcid = response.css(
            'input[name="Bcid"]::attr(value)').extract()
        url = '''https://www.harrods.com/en-gb/product/
                buyingcontrols/{}?pdpTemplateType={}
                &bcid={}&colour={}&_=1535695971886'''.format(

                )
