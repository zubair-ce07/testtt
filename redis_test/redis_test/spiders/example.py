# -*- coding: utf-8 -*-

import redis
import time
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.http import Request
from scrapy.spider import Spider


class Mixin(object):
    def start_requests(self):
        """Returns a batch of start requests from redis."""
        return self.next_requests()

    def next_requests(self):
        """Returns a request to be scheduled or none."""
        redis_cli = redis.Redis()
        while True:
            while redis_cli.exists("test"):
                url = redis_cli.lpop("test")
                url = url.decode("utf-8")
                yield Request(url=url, dont_filter=True)
            print("while loo")
            time.sleep(1)

    def setup_redis(self, crawler=None):
        """Setup redis connection and idle signal.
        This should be called after the spider has set its crawler object.
        """
        if crawler is None:
            # We allow optional crawler argument to keep backwards
            # compatibility.
            # XXX: Raise a deprecation warning.
            crawler = getattr(self, 'crawler', None)

        if crawler is None:
            raise ValueError("crawler is required")

        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def schedule_next_requests(self):
        """Schedules a request if available"""
        # TODO: While there is capacity, schedule a batch of redis requests.
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        # XXX: Handle a sentinel to close the spider.
        self.schedule_next_requests()
        raise DontCloseSpider


class RedisSpider(Mixin, Spider):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super(RedisSpider, cls).from_crawler(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj


class example(RedisSpider):
    name = "example"

    def parse(self, response):
        item = {}
        print(response.url)
        print("end")
        item["url"] = response.url

        yield item
