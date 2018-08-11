# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SheegoproductsSpider(CrawlSpider):
    name = 'sheegoproducts'
    allowed_domains = ['sheego.de']
    start_urls = ['http://sheego.de/']
    rules = (
            Rule(LinkExtractor(
                allow=('(\w)*'),
                deny=('/neu/', '/inspiration/',
                 '/damenmode-sale/', '/magazin/'),
                restrict_css='.cj-mainnav'),
                callback='parse_categories',),
            )
    
    def parse_categories(self, response):
        categories = self.get_categories(response)
        for category in categories:
            url = response.urljoin("?filterSHKategorie={}".format(category))
            yield scrapy.Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        product_urls = self.get_products_urls(response)
        for url in product_urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        pass
    
    def get_categories(self, response):
        return response.css(
            ".form-group--checkbox input::attr(value)").extract()

    def get_products_urls(self, response):
        return response.css(
            ".js-product__link::attr(href)").extract()
