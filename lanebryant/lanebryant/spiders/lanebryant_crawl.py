from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from lanebryant.lanebryant_parser import ProductParser


class LanebryantCrawlSpider(CrawlSpider):
    name = 'lanebryant-crawl'
    allowed_domains = ['www.lanebryant.com']
    lanebryant_parser = ProductParser()
    start_urls = [
        'http://www.lanebryant.com/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css="[role='navigation']")),
        Rule(LinkExtractor(restrict_css='.mar-prd-item-image '), callback='parse_item'),
    )

    def parse(self, response):
        title = response.css('.mar-plp-header-title::text').extract_first()
        trail = response.meta.get('trail', [])
        trail.append([title, response.url])
        for request in super().parse(response):
            request.meta['trail'] = trail.copy()
            yield request

    def parse_item(self, response):
        return self.lanebryant_parser.parse(response)
