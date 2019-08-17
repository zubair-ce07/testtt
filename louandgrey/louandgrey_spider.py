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
    listing_css = ['.sub-nav', 'link[rel="next"]']

    rules = [
        Rule(link_extractor=LinkExtractor(restrict_css=product_css), callback='parse_product'),
        Rule(link_extractor=LinkExtractor(restrict_css=listing_css, tags=['a', 'link']), callback='parse'),
    ]

    def parse(self, response):
        requests = super(LouandgreySpider, self).parse(response)
        trail = self.add_trail(response)
        return [r.replace(meta={**r.meta, 'trail': trail}) for r in requests]

    def parse_product(self, response):
        return self.louandgrey_parser.parse(response)

    def add_trail(self, response):
        new_trail = [(response.css('head title::text').get(), response.url)]
        return response.meta.get('trail', []) + new_trail
