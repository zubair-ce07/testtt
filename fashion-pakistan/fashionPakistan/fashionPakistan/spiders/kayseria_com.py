# -*- coding: utf-8 -*-
import scrapy


class KayseriaComSpider(scrapy.Spider):
    name = 'kayseria.com'
    start_urls = ['https://www.kayseria.com/']

    def parse(self, response):
        pass
