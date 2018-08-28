from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .product_parser import Parser


class TerminalXSpider(CrawlSpider):
    name = "terminalx"
    parser = Parser()
    start_urls = [
        'https://www.terminalx.com/'
    ]
    allowed_domains = [
        'terminalx.com'
    ]

    product_css = ['.product-items']
    listing_css = ['.level2', '.pages-item-next']
    rules = (Rule(LinkExtractor(restrict_css=product_css), callback="parse_product"),
             Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             )

    def parse(self, response):
        trail = response.meta.get("trail", [])
        trail.append(response.url)

        for request in super(TerminalXSpider, self).parse(response):
            request.meta["trail"] = trail.copy()
            yield request

    def parse_product(self, response):
        return self.parser.parse(response)
