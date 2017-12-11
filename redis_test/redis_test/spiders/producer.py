# -*- coding: utf-8 -*-
import random
import time

import redis
import scrapy


class ProducerSpider(scrapy.Spider):
    name = "producer"
    allowed_domains = ["brainyquote.com"]
    start_urls = ['https://www.brainyquote.com/']

    def parse(self, response):
        redis_cli = redis.Redis()
        for url in response.css('#allTopics ::attr(href)').extract():
            redis_cli.lpush("test", response.urljoin(url))
            time.sleep(random.randrange(start=0, stop=10))

        return
