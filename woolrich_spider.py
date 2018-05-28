import datetime
import json
import time
import queue
import re
import requests
import scrapy
import ast
from collections import defaultdict
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class WoolrichSpider(CrawlSpider):
    name = 'woolrich_spider'
    allowed_domains = ['woolrich.eu']
    start_urls = ['http://www.woolrich.eu/en/gb/home']
    request_queue = queue.Queue()
    product = {}
    rules = [Rule(LinkExtractor(allow=(r'http://www.woolrich.eu/en/.*'), restrict_css='.menu-category'),
                                callback='crawl_page', follow=True),
             Rule(LinkExtractor(restrict_css='.product-name'), callback='parse_product')]

    def crawl_page(self, response):
        trail = (response.meta.get('trail') or [])
        for request in super().parse(response):
            page_title = response.css('title::text').extract_first()
            request.meta['trail'] = trail.copy() + [page_title, response.url]
            yield request

    def parse_product(self, response):
        self.product['retailer_sku'] = self.retailer_sku(response)
        self.product['uuid'] = "null"
        self.product['trail'] = response.meta.get('trail')
        self.product['url'] = response.url
        self.product['url_original'] = response.url
        self.product['name'] = self.product_name(response)
        self.product['price'] = self.product_price(response)
        self.product['brand'] = "woolrich"
        self.product['category'] = self.product_category(response)
        self.product['description'] = self.product_description(response)
        self.product['images'] = self.images(response)
        self.product['date'] = time.time()
        self.product['crawl_start_time'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        self.product['skus'] = defaultdict(list)
        colors_name = response.css('.swatch::text').extract()
        colors_link = response.css('.color>.selectable>a::attr(href)').extract()
        for index, value in enumerate(colors_link):
            request = scrapy.Request(colors_link[index], meta={'color': colors_name[index].strip()}, \
                                     callback=self.sizes)
            self.request_queue.put(request)
            yield request

    def product_description(self, response):
        return response.css('.description::text').extract_first().strip()

    def retailer_sku(self, response):
        return response.xpath('//*[@class="sku"]/@skuid').extract_first()

    def product_name(self, response):
        return response.css('.product-name::text').extract_first()

    def product_price(self, response):
        return response.css('.product-sales-price::text').extract_first()[1:]

    def product_category(self, response):
        return response.css('.breadcrumb>a::text').extract()

    def images(self, response):
        return response.xpath('//*[@class="productthumbnail"]/picture/img/@src').extract()

    def sizes(self, response):
        sizes_links = response.css('.size>.selectable>a::attr(href)').extract()
        for link in sizes_links:
            request = scrapy.Request(link, meta={'color': response.meta.get('color')}, callback=self.skus_maker)
            yield request

    def skus_maker(self, response):
        size_info = response.css('.size>.selected>a::text').extract_first().strip()
        stock_info = response.css('.in-stock-msg::text').extract_first() or 'Out of Stock'
        self.product['skus'][response.meta.get('color')].append({'size': size_info, \
                                                                 'stock_status': stock_info, \
                                                                 'price': self.product['price']})
        if self.request_queue.qsize() > 0:
            self.request_queue.get()
        else:
            yield self.product
