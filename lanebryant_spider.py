from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor

from lanebryant.spiders.lanebryant_parser import LaneBryantParser


class LaneBryantSpider(CrawlSpider):

    name = "lanebryant_spider"
    allowed_domains = ["lanebryant.com"]
    start_urls = ['http://www.lanebryant.com/']
    cookies = {
        'GEOLOCATION_INFO': 'CA|Canada|CAD'
    }

    listings_css = [
        "#asc-header-con",
        ".mar-pagination-section"
    ]
    products_css = [".inverted"]

    parse_spider = LaneBryantParser()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )

    def start_requests(self):
        return [Request(url, callback=self.parse, cookies=self.cookies, dont_filter=True) for url in self.start_urls]

    def parse_item(self, response):
        return self.parse_spider.parse(response)
