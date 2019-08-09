from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mooseknucklescanada.spiders.mkc_parser import MKCParser


class MKCCrawler(CrawlSpider):
    name = 'mkccrawler'
    mkc_parser = MKCParser()
    start_urls = [
        'https://www.mooseknucklescanada.com/en/'
    ]

    product_css = '.ls-products-grid__images'
    listing_css = ['.nav-primary', '.toolbar-bottom .next.i-next']

    rules = [
        Rule(link_extractor=LinkExtractor(restrict_css=product_css), callback='parse_product'),
        Rule(link_extractor=LinkExtractor(restrict_css=listing_css), callback='parse')
    ]

    def parse(self, response):
        requests = super(MKCCrawler, self).parse(response)
        trail = self.add_trail(response)

        return [r.replace(meta={**r.meta, 'trail': trail.copy()}) for r in requests]

    def parse_product(self, response):
        yield self.mkc_parser.parse(response)

    def add_trail(self, response):
        new_trail = (response.css('head title::text').get(), response.url)
        if not response.meta:
            return [new_trail]

        trail = response.meta.get('trail', [])
        trail.append(new_trail)

        return trail
