from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import w3lib.url as w3url

from .product_schema import Parser


class HugoBossSpider(CrawlSpider):
    name = "hugo_boss"
    parser = Parser()
    start_urls = [
        'https://www.hugoboss.com/us/'
    ]

    rules = (Rule(LinkExtractor(restrict_css='.swatch-list__image'), callback="parse_product"),
             Rule(LinkExtractor(restrict_css='.nav-list--third-level'), callback='parse', process_links='clean_links'),
             Rule(LinkExtractor(restrict_css='pagingbar__item'), callback='parse'),
             )

    def parse(self, response):
        trail = response.meta.get("trail", [])
        for request in super(HugoBossSpider, self).parse(response):
            request.meta["trail"] = trail.copy().append(response.url)
            yield request

    def parse_product(self, response):
        yield from self.parser.parse(response)

    @staticmethod
    def clean_links(links):
        for link in links:
            link.url = w3url.url_query_cleaner(link.url)
            yield link
