# -*- coding: utf-8 -*-
import scrapy


class BlueflySpider(scrapy.Spider):
    name = "bluefly"
    allowed_domains = ["bluefly.com"]
    start_urls = (
        'http://www.bluefly.com/',
    )

    def parse(self, response):
        pass
