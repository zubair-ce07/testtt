# -*- coding: utf-8 -*-
import random
import time

import redis
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.http import Request
from scrapy.spider import Spider


class RedisSpider(Spider):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super(RedisSpider, cls).from_crawler(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj

    def start_requests(self):
        """Returns a batch of start requests from redis."""
        return self.next_requests()

    def next_requests(self):
        redis_cli = redis.Redis()
        while True:
            # eventloop
            while redis_cli.exists("test"):
                url = redis_cli.lpop("test")
                url = url.decode("utf-8")
                yield Request(url=url, dont_filter=True)
            time.sleep(random.randrange(start=0, stop=10))

    def setup_redis(self, crawler=None):
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def schedule_next_requests(self):
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        self.schedule_next_requests()
        raise DontCloseSpider


class Consumer(RedisSpider):
    name = "consumer"

    def parse(self, response):
        item = dict()
        item["url"] = response.url
        yield item
