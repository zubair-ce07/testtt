# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class GarageSpider(scrapy.Spider):
    name = 'garage'
    allowed_domains = ['garageclothing.com']
    start_urls = ['http://garageclothing.com/ca']

    def start_requests(self):
        yield SplashRequest(
            url='http://quotes.toscrape.com/js/',
            callback=self.parse,
        )

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield{
                'text' : quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags > a.tag::text').extract()
            }