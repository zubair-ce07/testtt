# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .beyond_limits_parser import BeyondParserSpider

class BeyondLimitsSpider(CrawlSpider):
    name = 'beyondlimits'
    allowed_domains = ['beyondlimits.com']
    start_urls = ['https://www.beyondlimits.com/']
    product_parser = BeyondParserSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=('.bb_catnav--list'), deny=[r'/de/']), callback='parse_category'),
    )

    def parse_category(self, response):
        next_page = response.css(".bb_pagination--item.next::attr(href)").get()
        products = response.css(".bb_product--link.bb_product--imgsizer::attr(href)").getall()
        for product in products:
            yield response.follow(product, self.product_parser.parse_product)
        if next_page:
            yield response.follow(next_page, self.parse_category)
