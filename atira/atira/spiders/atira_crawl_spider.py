from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from atira.spiders.atira_parse_spider import AtiraParseSpider

class AtiraCrawlSpider(CrawlSpider):
    name = "atira"
    start_urls = [
        'https://atira.com/'
    ]

    listings_css = ['.ubermenu-item-level-2 a']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_item'),
    )

    item_parser = AtiraParseSpider()

    def parse_item(self, response):
        return self.item_parser.parse(response)
