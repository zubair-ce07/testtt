import scrapy
import json
import time
import datetime
import queue
import re
import sys
from ast import literal_eval
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class JacklemkusSpider(CrawlSpider):
    crawl_start_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    name = 'jacklemkus'
    allowed_domains = ['jacklemkus.com']
    start_urls = ['https://www.jacklemkus.com']
    product = {}
    trail_urls = []
    rules = [Rule(LinkExtractor(allow=[r'https://www.jacklemkus.com/(apparel|sneakers|headwear|accessories|kids)/.*/.*']),
                  callback='parse_products'),
             Rule(LinkExtractor(allow=[r'https://www.jacklemkus.com/']), callback='crawl_page', follow=True)]

    def crawl_page(self, response):
        self.trail_urls.append(response.url)

    def parse_products(self, response):
        self.extract_retailer_sku(response)
        self.product['uuid'] = 'null'
        self.product['trail'] = self.trail_urls
        self.trail_urls = self.trail_urls[:-1]
        self.extract_gender(response)
        self.extract_category(response)
        self.product['industry'] = 'null'
        self.extract_brand(response)
        self.extract_original_url(response)
        self.extract_price(response)
        self.extract_images(response)
        self.extract_product_skus(response, self.product['price'])
        self.extract_url(response)
        self.extract_name(response)
        self.extract_description(response)
        self.product['date'] = time.time()

        yield self.product

    def extract_retailer_sku(self, response):
        self.product['retailer_sku'] = response.css('.sku::text').extract_first()

    def extract_category(self, response):
        self.product['category'] = response.css('.breadcrumbs li:nth-child(2)>a::text').extract_first()

    def extract_original_url(self, response):
        self.product['url_original'] = response.url

    def extract_gender(self, response):
        product_details = response.css('td:last-child::text').extract()
        self.product['gender'] = product_details[0]

    def extract_price(self, response):
        product_price = re.findall("var optionsPrice = new Product.OptionsPrice(.+?);\n", response.body.decode('utf-8'), re.S)
        price_details = json.loads(product_price[0][1:-1])
        self.product['price'] = price_details['productPrice']

    def extract_images(self, response):
        self.product['image_urls'] = response.css('.hidden-xs img::attr(src)').extract()

    def extract_product_skus(self, response, product_price):
        skus = []
        raw_skus = response.xpath('//*[@class="product-data-mine"]/@data-lookup').extract_first()
        raw_skus = literal_eval(raw_skus)
        for value in raw_skus.values():
            skus.append({'price': product_price, 'currency': 'ZAR', 'size': value['size'], \
                         'sku_id': value['id'], 'out_of_stock': value['stock_status']})
        self.product['skus'] = skus

    def extract_brand(self, response):
        self.product['brand'] = response.css('.product-name h1::text').extract_first()

    def extract_url(self, response):
        self.product['url'] = response.css('link[rel="canonical"]::attr(href)').extract_first()

    def extract_name(self, response):
        self.product['name'] = response.css('.product-name h1::text').extract_first()

    def extract_description(self, response):
        product_description = []
        product_details = response.css('td:last-child::text').extract()
        product_attributes = response.css('th:first-child::text').extract()
        product_description.append(self.product['name'])
        for index, value in enumerate(product_details):
            product_description.append(product_attributes[index])
            product_description.append(product_details[index])
        self.product['description'] = product_description
