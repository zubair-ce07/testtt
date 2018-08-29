from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from .piazza_product import ProductParser


class PiazzaSpider(CrawlSpider):
    name = "piazza-crawl"
    start_urls = [
        'https://www.piazzaitalia.it/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=('.item.pages-item-next', '.level-top', '.level1')), callback='parse'),
        Rule(LinkExtractor(restrict_css=('.product-item-link',)), callback='parse_product'),
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
