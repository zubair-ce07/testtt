from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .bonmarche_product import ProductParser


class PiazzaSpider(CrawlSpider):
    name = "bonmarche-crawl"
    start_urls = [
        'https://www.bonmarche.co.uk/',
    ]
    css = '.name-level-3', '.name-level-1', '.page-next'
    rules = (
        Rule(LinkExtractor(restrict_css=css), callback='parse'),
        Rule(LinkExtractor(restrict_css=('.product-name',)), callback='parse_product'),
    )

    product_parser = ProductParser()

    def parse(self, response):
        trail = response.meta.get('trail', [])
        trail.append(response.url)
        for req in super().parse(response):
            trail_ = trail.copy()
            req.meta['trail'] = trail_
            yield req

    def parse_product(self, response):
        return self.product_parser.parse(response)
