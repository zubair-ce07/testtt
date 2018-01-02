import copy
import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from SchwabSpider.spiders.mixin import Mixin
from SchwabSpider.spiders.product import ProductSpider
from SchwabSpider.items import SchwabProduct



class SchwabSpider(CrawlSpider, Mixin):
    name = 'schwab_spider'
    productSpider = ProductSpider()
    url_regex = re.compile('"url":.*?"(.*?)".*?')
    rules = (
        Rule(LinkExtractor(
            restrict_css='.js-next'),
            callback='parse_categories'),
        Rule(LinkExtractor(
            restrict_css='.js-pl-product'),
            callback=productSpider.parse),
    )

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(start_url, callback=self.parse_menu)

    def parse_menu(self, response):
        jsonresponse = response.body_as_unicode()
        for url in self.url_regex.findall(jsonresponse):
            yield Request(url=url, callback=self.parse)

    def parse_categories(self, response):
        current_url = response.url
        for request in super().parse(response):
            trail = response.meta.get('trail', list())
            exist = [url for url in trail if url == current_url]
            if not exist:
                trail.append(response.url)
            request.meta['trail'] = trail

            yield request
