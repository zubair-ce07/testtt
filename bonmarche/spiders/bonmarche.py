from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor

from .bonmarche_product import ProductParser


class BonmarcheSpider(CrawlSpider):
    name = "bonmarche-crawl"
    start_urls = [
        # 'https://www.bonmarche.co.uk/',
        'https://www.bonmarche.co.uk/womens/clothing/jeans/',
    ]

    listing_css = ['.name-level-3', '.name-level-1']
    product_css = ['.product-name']

    rules = (
        # Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
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
        url = response.url
        return Request(url.split("?")[0], callback=self.product_parser.parse)
