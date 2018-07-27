# -*- coding: utf-8 -*-
from captchaMiddleware.middleware import RETRY_KEY

import scrapy
from scrapy.http.request import Request
import random

from .. import items
from .. import settings


class SearsSpider(scrapy.Spider):
    name = 'sears'
    start_urls = ['https://www.sears.com/en_us.html']
    base_url = "https://www.sears.com"
    category = None

    # def __init__(self):
    #     super(SearsSpider, self).__init__()
    #     print("Enter dropdown category name as follows:\n"
    #           "scrapy crawl sears -a category=Auto\n"
    #           "The category is case sensitive\n")

    def parse(self, response):
        category_urls = response.xpath('//ul[@class="gnf_clr "]//a/@href').extract()
        category_names = response.xpath('//ul[@class="gnf_clr "]//a//text()').extract()
        for (category_url, category_name) in zip(category_urls, category_names):
            category_url = self.base_url + category_url
            meta_data = {
                'main_category_name' : category_name,
                RETRY_KEY: 0
            }
            if self.category is None:
                 request = Request(category_url, self.parse_main_category, meta=meta_data)
                 request.meta['proxy'] = random.choice(settings.PROXY_ADDRESS_POOL)
                 yield request
            else:
                if category_name == self.category:
                    request = Request(category_url, self.parse_main_category, meta=meta_data)
                    request.meta['proxy'] = random.choice(settings.PROXY_ADDRESS_POOL)
                    yield request

    def parse_main_category(self, response):
        print("URL: " + response.request.url)