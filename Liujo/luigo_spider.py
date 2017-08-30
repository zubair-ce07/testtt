from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'luijo-it'
    market = 'IT'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/gb/']


class LiujoParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'


class LiujoCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = LiujoParseSpider()

    listing_css = [
        '.second-level [target="_self"]',
    ]

    pagination_css = '[rel="next"]::attr(href)'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css),
             callback='paging_request'),
    )

    def paging_request(self, response):
        for request in self.parse(response):
            yield request

        from termcolor import colored
        print(colored(response.url, 'red'))

        if response.css(self.pagination_css):
            yield Request(url=clean(response.css(self.pagination_css))[0], callback=self.paging_request)