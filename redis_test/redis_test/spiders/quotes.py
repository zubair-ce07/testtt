# -*- coding: utf-8 -*-
import redis
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["brainyquote.com"]
    start_urls = ['https://www.brainyquote.com//']

    def parse(self, response):
        redis_cli = redis.Redis()
        for url in response.css('#allTopics ::attr(href)').extract():
            redis_cli.lpush("test", response.urljoin(url))
            print("pushed url")

        return
