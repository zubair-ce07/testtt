from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from levi_pt.spiders.levi_parse_spider import LeviptParseSpider


class LeviptCrawlSpider(CrawlSpider):
    name = "levi"
    allowed_domains = ['levi.pt']
    start_urls = [
        'https://www.levi.pt/pt'
    ]
    listings_css = ['nav .main-entry ', '.pages .active +a']
    item_css = ['.thumbnail .ga-track-product ']
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse', follow=True),
        Rule(LinkExtractor(restrict_css=item_css), callback='parse_item'),

    )
    item_parser = LeviptParseSpider()

    def parse(self, response):
        requests = super().parse(response)
        trail = response.meta.get('trail', [])
        trail.append(response.url)
        for request in requests:
            request.meta['trail'] = trail.copy()
            yield request

    def parse_item(self, response):
        return self.item_parser.parse(response)
