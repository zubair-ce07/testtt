import datetime
import json
import re
import scrapy
import time
from ast import literal_eval
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class JacklemkusSpider(CrawlSpider):
    name = 'jacklemkus'
    allowed_domains = ['jacklemkus.com']
    start_urls = ['https://www.jacklemkus.com']
    rules = [Rule(LinkExtractor(restrict_css=(['#nav li>a'])), callback='crawl_page', follow=True),
             Rule(LinkExtractor(restrict_css=(['.product-name'])), callback='parse_products', follow=True)]

    def crawl_page(self, response, append=True):
        for request in super().parse(response):
            page_title = response.css('title::text').extract_first()
            request.meta['trail'] = (response.meta.get('trail') or []) + [page_title, response.url]
            yield request

    def parse_products(self, response):
        product = {}
        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['uuid'] = 'null'
        product['trail'] = response.meta.get('trail')
        product['gender'] = self.extract_gender(response)
        product['category'] = self.extract_category(response)
        product['industry'] = 'null'
        product['brand'] = self.extract_brand(response)
        product['url_original'] = self.extract_original_url(response)
        product['price'] = self.extract_price(response)
        product['image_urls'] = self.extract_images(response)
        product['skus'] = self.extract_product_skus(response, product['price'])
        product['url'] = self.extract_url(response)
        product['name'] = self.extract_name(response)
        product['description'] = self.extract_description(response, product['name'])
        product['date'] = time.time()
        product['crawl_start_time'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        yield product

    def extract_retailer_sku(self, response):
        return response.css('.sku::text').extract_first()

    def extract_category(self, response):
        return response.css('.breadcrumbs li>a::text').extract()[1:]

    def extract_original_url(self, response):
        return response.url

    def extract_gender(self, response):
        return response.css('td:last-child::text').extract()[0]

    def extract_price(self, response):
        product_price = re.findall("var optionsPrice = new Product.OptionsPrice(.+?);\n", response.text, re.S)
        price_details = json.loads(product_price[0][1:-1])
        return price_details['productPrice']

    def extract_images(self, response):
        return response.css('.hidden-xs img::attr(src)').extract()

    def extract_product_skus(self, response, product_price):
        skus = []
        raw_skus = response.xpath('//*[@class="product-data-mine"]/@data-lookup').extract_first()
        raw_skus = literal_eval(raw_skus)
        for value in raw_skus.values():
            skus.append({'price': product_price, 'currency': 'ZAR', 'size': value['size'], \
                         'sku_id': value['id'], 'out_of_stock': value['stock_status']})
        return skus

    def extract_brand(self, response):
        return response.css('.product-name h1::text').extract_first()

    def extract_url(self, response):
        return response.css('link[rel="canonical"]::attr(href)').extract_first()

    def extract_name(self, response):
        return response.css('.product-name h1::text').extract_first()

    def extract_description(self, response, name):
        product_description = []
        product_description.append(name)
        for description in response.css('#product-attribute-specs-table tbody>tr'):
            product_description.append(description.css('th::text').extract_first())
            product_description.append(description.css('td::text').extract_first())
        return product_description
