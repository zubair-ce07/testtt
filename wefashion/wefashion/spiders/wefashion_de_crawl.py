from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner

from wefashion.wefashion_de_parse import ProductParser


class WefashionDeCrawlSpider(CrawlSpider):
    name = 'wefashion-de-crawl'
    wefashion_parser = ProductParser()
    allowed_domains = ['www.wefashion.de']
    start_urls = [
        'http://www.wefashion.de/'
    ]
    listing_css = [
        '.header-top-level-menu',
        '#category-level-0'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css='.product-image',
                           process_value=url_query_cleaner),
             callback='parse_item'),
    )

    def parse(self, response):
        title = response.css('.refinement-header::text').extract_first(default='').strip()
        trail = response.meta.get('trail', [])
        trail.append([title, response.url])

        for request in super().parse(response):
            request.meta['trail'] = trail.copy()
            yield request

    def parse_item(self, response):
        return self.wefashion_parser.parse(response)
