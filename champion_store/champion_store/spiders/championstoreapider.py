# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .productparser import ProductParser


class ChampionStoreSpider(CrawlSpider):
    name = 'championStore'
    product_parser = ProductParser()
    allowed_domains = ['championstore.com']
    start_urls = ['http://championstore.com/']

    rules = (
        Rule(LinkExtractor(allow=r'en/champion/', restrict_css=('.departmentMenu', )),
             callback='parse_page', follow=False),
    )

    def parse_page(self, response):
        product_urls = response.css('.product_name a::attr(href)').getall()

        for url in product_urls:
            yield Request(url=url, callback=self.product_parser.parse, meta={'trail': [response.url]})

