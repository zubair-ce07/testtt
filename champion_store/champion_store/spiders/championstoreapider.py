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

    ALLOW = r'en/champion/'
    RESTRICT_CSS = ('.departmentMenu',)

    rules = (
        Rule(LinkExtractor(allow=ALLOW, restrict_css=RESTRICT_CSS), callback='parse_product_requests'),
    )

    def parse_product_requests(self, response):
        total_items = response.css('.pagination_present .title::text').get()

        if not total_items:
            return self.parse_product(response)

        query_params = {'beginIndex': '0', 'pageSize': total_items.strip()}
        url = add_or_replace_parameters(response.url, query_params)
        return Request(url=url, callback=self.parse_product, dont_filter=True)

    def parse_product(self, response):
        product_urls = response.css('.product_name a::attr(href)').getall()
        requests = [Request(url=url, callback=self.product_parser.parse, meta={'trail': [response.url]})
                    for url in product_urls]

        for request in requests:
            yield request
