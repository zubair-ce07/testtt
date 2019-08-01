from w3lib.url import add_or_replace_parameter

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from louandgrey.spiders.louandgrey_parser import LouandgreyParser


class LouandgreySpider(CrawlSpider):
    name = 'louandgreyspider'
    louandgrey_parser = LouandgreyParser()
    start_urls = [
        'https://www.louandgrey.com/'
    ]

    rules = [
        Rule(link_extractor=LinkExtractor(restrict_css='li.product .product-wrap a[data-page]'),
             callback='parse_product'),
        Rule(link_extractor=LinkExtractor(restrict_css='.sub-nav'), callback='parse_listing')
    ]

    def parse(self, response):
        requests = super(LouandgreySpider, self).parse(response)
        for request in requests:
            request.meta['trail'] = self.louandgrey_parser.add_trail(response)
            yield request

    def parse_listing(self, response):
        pages_count = int(response.css('.product-listing input[name="pages"]::attr(value)').get())
        for index in range(1, pages_count+1):
            yield Request(url=add_or_replace_parameter(response.url, 'goToPage', index),
                          meta={'trail': self.louandgrey_parser.add_trail(response)})

    def parse_product(self, response):
        yield self.louandgrey_parser.parse(response)
