import copy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# from .mixin import Mixin
from JosephSpider.spiders.parse import ParseSpider
from JosephSpider.spiders.mixin import Mixin


class JosephSpider(CrawlSpider, Mixin):
    name = 'joseph_spider'
    parse_spider = ParseSpider()

    rules = (
        Rule(LinkExtractor(
            restrict_css='a[class*="navigation__link"]'), callback='parse'),
        Rule(LinkExtractor(restrict_css='.search-result-content .thumb-link'),
             callback=parse_spider.parse),
    )

    def parse(self, response):
        for request in super().parse(response):
            product = response.meta.get('product', dict())
            new_product = copy.deepcopy(product)
            new_product['trail'] = product.get('trail', list())
            new_product['trail'].append(response.url)
            request.meta['product'] = new_product
            yield request
