from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .bonmarche_product import ProductParser


class BonmarcheSpider(CrawlSpider):
    name = "bonmarche-crawl"
    start_urls = [
        'https://www.bonmarche.co.uk/',
    ]

    listing_css = ['.name-level-3', '.name-level-1']
    product_css = ['.product-name']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css, process_value=
             lambda x: x.split("?")[0]), callback='parse_product'),
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
