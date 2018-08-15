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

    product_selectors = ['.swatch-list__image']
    crawl_selectors = ['.nav-list--third-level', '.pagingbar__item']

    rules = (Rule(LinkExtractor(restrict_css=product_selectors, process_value=w3cleaner), callback="parse_product"),
             Rule(LinkExtractor(restrict_css=crawl_selectors), callback='parse'),
             )

    def parse(self, response):
        trail = response.meta.get("trail", [])
        trail.append(response.url)
        for request in super(HugoBossSpider, self).parse(response):
            request.meta["trail"] = trail.copy()
            yield request

    def parse_product(self, response):
        return self.parser.parse(response)
