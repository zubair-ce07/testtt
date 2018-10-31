import json

from scrapy import Request
from w3lib.url import url_query_parameter
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .productparser import ProductParser


class AlcottSpider(CrawlSpider):
    productparser = ProductParser()
    name = 'alcott-crawler'
    allowed_domains = ['alcott.eu']
    start_urls = ['https://www.alcott.eu/en/catalogo']
    url_query = '/ProductListingView?categoryId={}&storeId={}'
    sub_menu = '.submenu-item'
    product = '.product_name'

    rules = (
        Rule(LinkExtractor(restrict_css=(sub_menu)), callback='parse'),
        Rule(LinkExtractor(restrict_css=(product)),
             callback=productparser.parse),
    )

    def parse(self, response):
        category = url_query_parameter(response.url, "categoryId")
        storeId = url_query_parameter(response.url, "storeId")

        if not(category and storeId):
            url = response.url + self.query(response)
            req = Request(url=url, callback=self.parse)
            yield req

        yield from super(AlcottSpider, self).parse(response)

    def query(self, response):
        css = '[name=storeId]::attr(value)'
        store_id = response.css(css).extract_first()

        css = '[name=pageId]::attr(content)'
        category_id = response.css(css).extract_first()

        return self.url_query.format(category_id, store_id)
