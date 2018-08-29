from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner as w3cleaner

from .hugoboss_parser import Parser


class HugobossSpider(CrawlSpider):
    name = "hugoboss"
    parser = Parser()

    start_urls = [
        'https://www.hugoboss.com/us/'
    ]

    allowed_domains = [
        'hugoboss.com'
    ]

    product_css = ['.swatch-list__image']
    listing_css = ['.nav-list--third-level', '.pagingbar__item']

    rules = (Rule(LinkExtractor(restrict_css=product_css, process_value=w3cleaner), callback="parse_product"),
             Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             )

    def parse(self, response):
        trail = response.meta.get("trail", [])
        trail.append(response.url)
        for request in super(HugobossSpider, self).parse(response):
            request.meta["trail"] = trail.copy()
            yield request

    def parse_product(self, response):
        return self.parser.parse(response)
