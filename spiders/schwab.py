import copy
import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from SchwabSpider.spiders.mixin import Mixin
from SchwabSpider.spiders.product import ProductSpider


class SchwabSpider(CrawlSpider, Mixin):
    name = 'schwab_spider'
    productSpider = ProductSpider()
    url_regex = re.compile('"url":.*?"(.*?)".*?')
    rules = (
        Rule(LinkExtractor(
            restrict_css='.js-next'),
            callback='parse_links'),
        Rule(LinkExtractor(
            restrict_css='.js-pl-product'),
            callback=productSpider.parse),
    )

    def parse(self, response):
        if response.url == self.start_urls[0]:
            jsonresponse = response.body_as_unicode()
            for url in self.url_regex.findall(jsonresponse):
                yield Request(url=url, callback=self.parse)

        requests = super().parse(response)
        for request in requests:
            yield request

    def parse_links(self, response):
        current_url = response.url
        for request in super().parse(response):
            product = response.meta.get('product', dict())
            new_product = copy.deepcopy(product)
            new_product['trail'] = product.get('trail', list())
            trail = new_product.get('trail')
            exist = [url for url in trail if url == current_url]
            if not exist:
                trail.append(response.url)
            request.meta['product'] = new_product

            yield request
