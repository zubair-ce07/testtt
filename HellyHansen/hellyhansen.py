# -*- coding: utf-8 -*-
import scrapy
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
        products = response.css(".b-products__item.item.product.product-item a::attr(href)").getall()
        for product in products:
            yield response.follow(product, self.product_parser.parse_product)

        loaded_page = response.meta.get("p", 1)
        data_pages = response.css(".b-toolbar.b-toolbar--bottom .infinite-scrolling::attr(data-page-count)").get()
        if data_pages and (int(data_pages) > loaded_page):
            loaded_page += 1
            url = w3lib.url.add_or_replace_parameter(response.request.url, 'p', loaded_page)
            request = scrapy.Request(url, callback=self.parse)
            request.meta['p'] = loaded_page
            yield request
