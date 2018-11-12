# -*- coding: utf-8 -*-
import scrapy


class BonanzasatrangiComSpider(scrapy.Spider):
    name = 'bonanzasatrangi.com'
    start_urls = ['https://www.bonanzasatrangi.com/pk/']

    def parse(self, response):
        pass
