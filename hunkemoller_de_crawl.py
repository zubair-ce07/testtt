from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from hunkemoller.ProductParser import ProductParser


class HunkemollerDeCrawlSpider(CrawlSpider):
    name = 'hunkemoller-de-crawl'
    product = ProductParser()
    start_urls = [
        'https://www.hunkemoller.de/de_de'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=['.nav-container', '.pages']), follow=True),
        Rule(LinkExtractor(restrict_css='.product-image'), callback='parse_item'),
    )

    def parse_item(self, response):
        trail = ['', response.request.headers.get('Referer', None).decode('utf-8')]
        response.request.meta['trail'] = trail
        return self.product.parse(response)
