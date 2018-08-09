from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from hunkemoller.ProductParser import ProductParser


class HunkemollerDeCrawlSpider(CrawlSpider):
    name = 'hunkemoller-de-crawl'
    parser = ProductParser()
    allowed_domains = ['www.hunkemoller.de']
    start_urls = [
        'https://www.hunkemoller.de/de_de'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=['.nav-container', '.pages', '.color-options']), callback='parse'),
        Rule(LinkExtractor(restrict_css='.product-image'), callback='parse_item'),
    )

    def parse(self, response):
        requests = super(HunkemollerDeCrawlSpider, self).parse(response)
        title = response.css('.parent-title span::text').extract_first(default='')
        trail = response.meta.get('trail', [])
        trail.append([title, response.url])

        for request in requests:
            request.meta['trail'] = trail.copy()
            yield request

    def parse_item(self, response):
        return self.parser.extract_retailer_sku(response)
