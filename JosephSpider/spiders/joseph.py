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
        Rule(LinkExtractor(
            restrict_css='.navigation__item2 a.desktop-media'),
            callback='parse'),
        Rule(LinkExtractor(
            restrict_css='.infinite-scroll-placeholder',
            tags=["div"], attrs=["data-grid-url"]),
            callback='parse'),
        Rule(LinkExtractor(restrict_css='.product-image .thumb-link'),
             callback=parse_spider.parse),
    )

    def parse(self, response):
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
