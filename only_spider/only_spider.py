from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from only.spiders.only_parser import OnlyParser

class OnlySpider(CrawlSpider):
    name = "only_spider"
    allowed_domains = ["only.com"]
    start_urls = ['https://www.only.com/gb/en/home']

    listings_css = [
        ".category-navigation__item",
        ".js-paging-controls-numbers"
    ]
    products_css = [".thumb-link"]

    parse_spider = OnlyParser()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse_item(self, response):
        return self.parse_spider.parse(response)
