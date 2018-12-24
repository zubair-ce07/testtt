from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from parse_items_structure import ParseItems


class DrmartensSpider(CrawlSpider):
    name = 'drmartens_au_spider'
    allowed_domains = ['www.drmartens.com.au']
    start_urls = ['http://www.drmartens.com.au/']
    parse_items = ParseItems()

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36'
    }

    listing_css = ['.column.main']
    heading_css = ['.main-menu']
    rules = [
        Rule(LinkExtractor(restrict_css=heading_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item')
    ]

    def parse(self, response):
        trail = self.parse_items.extract_trail(response)
        title = self.parse_items.extract_title(response)

        for request in super().parse(response):
            request.meta['trail'] = trail + [[title, response.url]]
            yield request

    def parse_item(self, response):
        return self.parse_items.extract_item(response)
