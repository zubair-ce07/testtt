from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from .bonmarche_product import ProductParser


class PiazzaSpider(CrawlSpider):
    name = "bonmarche-crawl"
    start_urls = [
        'https://www.bonmarche.co.uk/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=('.name-level-3', '.name-level-1', '.page-next')), callback='parse'),
        Rule(LinkExtractor(restrict_css=('.product-name',)), callback='parse_product'),
    )

    product_parser = ProductParser()

    def parse(self, response):
        requests = super().parse(response)
        for req in requests:
            trail = response.meta.get('trail', [])
            trail.append(response.url)
            req.meta['trail'] = list(set(trail))
            yield req

    def parse_product(self, response):
        return self.product_parser.parse(response)
