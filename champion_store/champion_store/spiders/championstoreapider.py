from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import Request
from w3lib.url import add_or_replace_parameters

from .productparser import ProductParser


class ChampionStoreSpider(CrawlSpider):
    name = 'championStoreCrawler'
    product_parser = ProductParser()
    allowed_domains = ['championstore.com']
    start_urls = ['http://championstore.com/']

    allow = r'en/champion/'
    listings_css = ('.departmentMenu',)

    rules = (
        Rule(LinkExtractor(allow=allow, restrict_css=listings_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        total_items = response.css('.pagination_present .title::text').get()

        if not total_items:
            return self.parse_products(response)

        query_params = {'beginIndex': '0', 'pageSize': total_items.strip()}
        url = add_or_replace_parameters(response.url, query_params)
        return Request(url=url, callback=self.parse_products, dont_filter=True)

    def parse_products(self, response):
        product_urls = response.css('.product_name a::attr(href)').getall()
        yield from [Request(url=url, callback=self.product_parser.parse, meta={'trail': [response.url]})
                    for url in product_urls]
