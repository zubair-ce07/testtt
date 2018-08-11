from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner as w3cleaner

from .product_parser import Parser


class HugoBossSpider(CrawlSpider):
    name = "hugoboss"
    parser = Parser()

    start_urls = [
        'https://www.hugoboss.com/us/'
    ]

    allowed_domains = [
        'hugoboss.com'
    ]

    rules = (Rule(LinkExtractor(restrict_css='.swatch-list__image', process_value=w3cleaner), callback="parse_product"),
             Rule(LinkExtractor(restrict_css=('.nav-list--third-level', 'pagingbar__item')), callback='parse'),
             )

    def parse(self, response):
        trail = response.meta.get("trail", [])
        for request in super(HugoBossSpider, self).parse(response):
            request.meta["trail"] = trail.copy()
            request.meta["trail"].append(response.url)
            yield request

    def parse_product(self, response):
        yield self.parser.parse(response)
