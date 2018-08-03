from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from .product_schema import Parser


class JoopSpider(CrawlSpider):
    name = "joop_de"
    parser = Parser()
    start_urls = [
        'https://joop.com/de/de/'
    ]
    rules = (Rule(LinkExtractor(restrict_css='.colors'), callback="parse_product", follow=True),
             Rule(LinkExtractor(restrict_css='#products'), callback="parse", follow=True),
             Rule(LinkExtractor(restrict_css='#mainnav'), callback="parse", follow=True),
             )

    def parse_product(self, response):
        yield self.parser.parse(response)
