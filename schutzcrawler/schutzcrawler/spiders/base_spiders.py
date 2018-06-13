import copy

from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider


class BaseParseSpider(Spider):
    def next_request_or_product(self, product):
        if product["requests"]:
            return product["requests"].pop()
        else:
            return product


class BaseCrawlSpider(CrawlSpider):
    def add_trail(self, response):
        trail = response.meta.get('trail', [])
        trail = copy.deepcopy(trail)
        trail.append(response.url)
        return trail
