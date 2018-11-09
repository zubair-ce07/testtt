# -*- coding: utf-8 -*-
import json
import re

from scrapy import Spider, Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_parameter, add_or_replace_parameter

from ..items import Item
from ..utilities import pricing


class BeaverBrooksParseSpider(Spider):
    name = 'beaverbrooks-parse'

    def parse(self, response):
        item = Item()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['name'] = self.extract_name(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        item['category'] = self.extract_category(response)
        item['url'] = self.extract_product_url(response)
        item['skus'] = self.extract_skus(response)

        return item

    def extract_currency(self, response):
        css = 'span[itemprop="priceCurrency"]::attr(content)'
        return response.css(css).extract_first()

    def extract_retailer_sku(self, response):
        css = 'meta[itemprop="sku"]::attr(content)'
        return response.css(css).extract()

    def extract_name(self, response):
        css = 'span#productName::text'
        return response.css(css).extract()

    def extract_brand(self, response):
        css = 'span[itemprop="brand"] > meta::attr(content)'
        return response.css(css).extract()

    def extract_image_urls(self, response):
        css = 'img[itemprop="image"]::attr(src)'
        return response.css(css).extract()

    def extract_care(self, response):
        css = ''
        return response.css(css).extract()

    def extract_description(self, response):
        css = 'p[itemprop="description"]::text, p[itemprop="description"] ~ p:first-of-type::text'
        return response.css(css).extract()

    def extract_money_strings(self, response):
        css = 'span[itemprop="price"]::attr(content), p.prod-price-was::text'
        return response.css(css).extract()

    def extract_category(self, response):
        css = ''
        return response.css(css).extract()

    def extract_product_url(self, response):
        css = 'meta[itemprop="url"]::attr(content)'
        return response.css(css).extract()
    
    def extract_skus(self, response):
        css = 'table.product-specification tr *::text'
        raw_care = response.css(css).extract()
        care = [value.strip + ' ' for value in raw_care]
        return care

class BeaverBrooksCrawlSpider(CrawlSpider):
    name = 'beaverbrooks-crawl'
    allowed_domains = ['beaverbrooks.co.uk']
    start_urls = ['http://beaverbrooks.co.uk/']

    count = 0

    listings_css = ['li.main-nav__item', 'ul.list-pagination']
    products_css = ['div.product-list__item']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), process_links='filter_query_based_links'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'),
    )

    product_parser = BeaverBrooksParseSpider()

    def filter_query_based_links(self, links):
        for link in links:
            query_checks = ['commonDiamondcut' in link.url, 'commonDiamondcarat' in link.url, 'price' in link.url]
            if not all(query_checks):
                yield link

    def parse_product(self, response):
        self.count+=1
        print('\n\n\n\n',self.count, '\n\n\n\n')
        # return self.product_parser.parse(response)
