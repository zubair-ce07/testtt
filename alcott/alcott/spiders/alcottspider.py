import json
import scrapy
import w3lib.url

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .productparser import ProductParser


class AlcottSpider(CrawlSpider):
    productparser = ProductParser()
    name = 'alcott-crawler'
    allowed_domains = ['alcott.eu']
    start_urls = ['https://www.alcott.eu/en/catalogo']
    rules = (
        Rule(
            LinkExtractor(restrict_css=('.submenu-item a')),
            callback='parse'),
        Rule(
            LinkExtractor(restrict_css=('.product_name a')),
            callback=productparser.parse),
    )

    def parse(self, response):
        category = w3lib.url.url_query_parameter(response.url, "categoryId")
        storeId = w3lib.url.url_query_parameter(response.url, "storeId")
        if not(category and storeId):
            url = response.url + self.query_string_data(response)
            req = scrapy.Request(url=url, method="GET", callback=self.parse)
            yield req

        yield from super(AlcottSpider, self).parse(response)

    def query_string_data(self, response):
        css = '*[name=storeId]::attr(value)'
        store_id = response.css(css).extract_first()

        css = '*[name=pageId]::attr(content)'
        category_id = response.css(css).extract_first()

        return '/ProductListingView?categoryId='+category_id+'&storeId='+store_id
