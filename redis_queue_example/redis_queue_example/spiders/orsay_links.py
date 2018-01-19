# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from redis import Redis
from scutils.redis_queue import RedisQueue
import time


class OrsayLinksSpider(CrawlSpider):
    name = 'orsay_links'
    start_urls = ['http://orsay.com/']
    allowed_domains = ['orsay.com']
    rules = (
        Rule(LinkExtractor(restrict_css=
                           '#nav > .level0 > .level0 > .level1'),
             follow=True),
        Rule(LinkExtractor(restrict_css=
                           '.toolbar-top ul.pagination .next.i-next'),
             follow=True),
        Rule(LinkExtractor(restrict_css=
                           '#products-list > .item .product-image-wrapper'),
             callback='parse_product', follow=True),
    )

    def parse_product(self, response):
        redis_conn = Redis()
        queue = RedisQueue(redis_conn, "item")
        time.sleep(2)
        queue.push(response.url)
