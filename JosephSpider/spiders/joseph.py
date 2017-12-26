import copy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .mixin import Mixin
from .parse import ParseSpider


class JosephSpider(CrawlSpider):
    name = 'joseph_spider'
    mixin = Mixin()
    allowed_domains = mixin.allowed_domains
    start_urls = mixin.start_urls
    parse_spider = ParseSpider()

    rules = (
        Rule(LinkExtractor(
            restrict_css='a[class*="navigation__link"]'), callback='parse'),
        Rule(LinkExtractor(restrict_css='.search-result-content .thumb-link'),
             callback=parse_spider.parse_product),
    )

    def parse(self, response):

        for request in super().parse(response):
            data = response.meta.get('data') or dict()
            data = copy.deepcopy(data)
            data['trail'] = data.get('trail') or list()
            data['trail'].append(request.url)
            request.meta['data'] = data
            yield request
