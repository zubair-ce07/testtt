# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class DamallSpider(CrawlSpider):
    name = 'Damall'
    allowed_domains = ['damart.co.uk']
    start_urls = ['http://damart.co.uk/']
    rules = (
            Rule(LinkExtractor(
                allow=('\d'),
                restrict_css='.ss_menu_bloc'),
                callback='parse_listing',),
            )

    def parse_listing(self, response):
        product_urls = get_products_urls(response)
        for url in product_urls:
            yield scrapy.Request(url=url callback=self.parse_product)

    def parse_product(self, response):
        pass

    def get_products_urls(self, response):
        urls = response.css(".ss_menu_bloc a::attr(href)").extract()
        return [response.urljoin(url) for ulr in urls]
