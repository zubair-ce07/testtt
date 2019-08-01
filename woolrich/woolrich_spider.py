from w3lib.url import add_or_replace_parameters

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from woolrich.spiders.woolrich_parser import WoolrichParser


class WoolrichSpider(CrawlSpider):
    name = 'woolrichspider'
    woolrich_parser = WoolrichParser()
    start_urls = [
        'https://www.woolrich.eu/en/gb/home'
    ]

    rules = [
        Rule(link_extractor=LinkExtractor(restrict_css='a.thumb-link'), callback='parse_item'),
        Rule(link_extractor=LinkExtractor(restrict_css='.marked a.has-sub-menu'), callback='parse_listing')
    ]

    def parse(self, response):
        requests = super(WoolrichSpider, self).parse(response)
        for request in requests:
            request.meta['trail'] = self.woolrich_parser.add_trail(response)
            yield request

    def parse_listing(self, response):
        products_on_page, remaining_products = self.get_page_metadata(response)
        requests_count = remaining_products // products_on_page + 1
        for index in range(0, requests_count):
            params = {
                'sz': products_on_page,
                'start': products_on_page * index
            }
            yield Request(url=add_or_replace_parameters(response.url, params),
                          meta={'trail': self.woolrich_parser.add_trail(response)})

    def parse_item(self, response):
        yield self.woolrich_parser.parse(response)

    def get_page_metadata(self, response):
        css = '.search-result-content::attr({})'
        page_result = response.css(f'{css.format("data-pagesize")}, {css.format("data-searchcount")}').getall()
        return list(map(int, page_result))
