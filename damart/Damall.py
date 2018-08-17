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
        pass
