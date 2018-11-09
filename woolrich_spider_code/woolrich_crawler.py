# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from woolrich.woolrich_parse_product import WoolrichParseProduct


class WoolrichSpider(CrawlSpider):
    name = 'woolrich_crawler'
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com/']
    allow_r = '.com/([a-z-]+$)|(.*page)'
    listings_css = ['#primary', '.pagination-item--next']
    product_css = '.card'
    product_parser = WoolrichParseProduct()

    rules = (
        Rule(LinkExtractor(allow=(allow_r), restrict_css=(listings_css)),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=(product_css)),
             callback=product_parser.parse_product),
    )

