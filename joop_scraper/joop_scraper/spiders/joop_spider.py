from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner as url_cleaner

from .product_schema import Parser


class JoopSpider(CrawlSpider):
    name = "joop"
    parser = Parser()

    start_urls = [
        'https://joop.com/de/de/'
    ]

    allowed_domains = [
        'joop.com'
    ]

    rules = (Rule(LinkExtractor(restrict_css='#products', process_value=url_cleaner), callback="parse_product"),
             Rule(LinkExtractor(restrict_css='#mainnav'), callback='parse'),
             )

    def parse(self, response):
        trail = response.meta.get("trail", [])
        for request in super(JoopSpider, self).parse(response):
            request.meta["trail"] = trail.copy()
            request.meta["trail"].append(response.url)
            yield request

    def parse_product(self, response):
        yield from self.parser.parse(response)

