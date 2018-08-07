from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from hunkemoller.ProductParser import ProductParser


class HunkemollerDeCrawlSpider(CrawlSpider):
    name = 'hunkemoller-de-crawl'
    parser = ProductParser()
    start_urls = [
        'https://www.hunkemoller.de/de_de'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=['.nav-container', '.pages']), follow=True, callback='parse'),
        Rule(LinkExtractor(restrict_css='.product-image'), callback='parse_item'),
    )

    def parse(self, response):
        total_requests = super().parse(response)
        for request in total_requests:
            title = response.css('.parent-title span::text').extract_first() or ''
            trail = response.request.meta.get('trail', [])
            trail.append([title, response.url])
            request.meta['trail'] = trail
            yield request

    def parse_item(self, response):
        return self.parser.parse(response)

