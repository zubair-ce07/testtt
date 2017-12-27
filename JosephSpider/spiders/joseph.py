from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# from .mixin import Mixin
from JosephSpider.spiders.parse import ParseSpider
from JosephSpider.spiders.mixin import Mixin


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
             callback=parse_spider.parse),
    )

    def parse(self, response):
        for request in super().parse(response):
            trail = response.meta.get('trail', list())
            trail.append(response.url)
            request.meta['trail'] = trail
            yield request
