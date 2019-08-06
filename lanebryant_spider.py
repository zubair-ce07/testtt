from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from lanebryant.spiders.lanebryant_parser import LaneBryantParser


class LaneBryantSpider(CrawlSpider):

    name = "lanebryant_spider"
    allowed_domains = ["lanebryant.com"]
    start_urls = ["http://www.lanebryant.com/"]

    listings_css = [
        "#asc-header-con",
        ".mar-pagination-section"
    ]
    products_css = [".inverted", ]

    parse_spider = LaneBryantParser()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse_item(self, response):
        return self.parse_spider.parse(response)
