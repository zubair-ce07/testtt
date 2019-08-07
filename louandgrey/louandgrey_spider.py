from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from louandgrey.spiders.louandgrey_parser import LouandgreyParser


class LouandgreySpider(CrawlSpider):
    name = 'louandgreyspider'
    louandgrey_parser = LouandgreyParser()
    start_urls = [
        'https://www.louandgrey.com/'
    ]

    allowed_domains = [
        'louandgrey.com',
        'anninc.scene7.com'
    ]

    product_css = '.product-wrap a[data-page]'
    next_page_css = 'link[rel="next"]'
    listing_css = '.sub-nav'

    rules = [
        Rule(link_extractor=LinkExtractor(restrict_css=product_css), callback='parse_product'),
        Rule(link_extractor=LinkExtractor(restrict_css=next_page_css)),
        Rule(link_extractor=LinkExtractor(restrict_css=listing_css))
    ]

    def parse(self, response):
        requests = super(LouandgreySpider, self).parse(response)
        trail = self.louandgrey_parser.add_trail(response)

        return [r.replace(meta={**r.meta,'trail': trail.copy()}) for r in requests]

    def parse_product(self, response):
        yield self.louandgrey_parser.parse(response)
