from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import w3lib.url as w3url

from .product_schema import Parser


class JoopSpider(CrawlSpider):
    name = "joop_de"
    parser = Parser()
    start_urls = [
        'https://joop.com/de/de/'
    ]

    @staticmethod
    def clean_links(links):
        for link in links:
            link.url = w3url.url_query_cleaner(link.url)
            yield link

    rules = (Rule(LinkExtractor(restrict_css='#products'), callback="parse_product", process_links='clean_links'),
             Rule(LinkExtractor(restrict_css='#mainnav'), callback='parse'),
             )

    def parse(self, response):
        trail = response.meta.get("trail", []).copy()
        trail.append(response.url)
        for request in super(JoopSpider, self).parse(response):
            request.meta["trail"] = trail
            yield request

    def parse_product(self, response):
        yield from self.parser.parse(response)
