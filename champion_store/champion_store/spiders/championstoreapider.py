from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import add_or_replace_parameters

from .productparser import ProductParser


class ChampionStoreSpider(CrawlSpider):
    name = 'championStore'
    product_parser = ProductParser()
    allowed_domains = ['championstore.com']
    start_urls = ['http://championstore.com/']

    rules = (
        Rule(LinkExtractor(allow=r'en/champion/', restrict_css=('.departmentMenu', )),
             callback='make_all_products_request', follow=False),
    )

    def make_all_products_request(self, response):
        url = ''
        total_items = response.css('.pagination_present .title::text').get()

        if total_items:
            query_params = {'beginIndex': '0', 'pageSize': total_items.strip()}
            url = add_or_replace_parameters(response.url, query_params)

        return Request(url=url if url != '' else response.url,
                       callback=self.parse_product, dont_filter=True)

    def parse_product(self, response):
        product_urls = response.css('.product_name a::attr(href)').getall()

        for url in product_urls:
            yield Request(url=url, callback=self.product_parser.parse, meta={'trail': [response.url]})

