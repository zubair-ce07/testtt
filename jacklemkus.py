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
    rules = [Rule(LinkExtractor(restrict_css=['#nav', '.ias_trigger']), callback='parse', follow=True),
             Rule(LinkExtractor(restrict_css='.product-name'), callback='parse_products', follow=True)]

    def parse(self, response, append=True):
        trail = (response.meta.get('trail') or [])
        for request in super().parse(response):
            page_title = response.css('title::text').extract_first()
            request.meta['trail'] = trail.copy() + [page_title, response.url]
            yield request

    def parse_products(self, response):
        product = {}
        product['retailer_sku'] = self.retailer_sku(response)
        product['uuid'] = 'null'
        product['trail'] = response.meta.get('trail')
        product['gender'] = self.gender(response)
        product['category'] = self.category(response)
        product['industry'] = 'null'
        product['brand'] = self.brand(response)
        product['url_original'] = self.original_url(response)
        product['price'] = self.price(response)
        product['image_urls'] = self.images(response)
        product['skus'] = self.product_skus(response, product['price'])
        product['url'] = self.url(response)
        product['name'] = self.product_name(response)
        product['description'] = self.description(response, product['name'])
        product['date'] = time.time()
        product['crawl_start_time'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        yield product

    def retailer_sku(self, response):
        return response.css('.sku::text').extract_first()

    def category(self, response):
        return response.css('.breadcrumbs li>a::text').extract()[1:]

    def original_url(self, response):
        return response.url

    def gender(self, response):
        return response.css('td:last-child::text').extract()[0]

    def price(self, response):
        product_price = re.findall("var optionsPrice = new Product.OptionsPrice(.+?);\n", response.text, re.S)
        price_details = json.loads(product_price[0][1:-1])
        return price_details['productPrice']

    def images(self, response):
        return response.css('.hidden-xs img::attr(src)').extract()

    def product_skus(self, response, product_price):
        skus = []
        raw_skus = response.xpath('//*[@class="product-data-mine"]/@data-lookup').extract_first()
        raw_skus = literal_eval(raw_skus)
        for value in raw_skus.values():
            skus.append({'price': product_price, 'currency': 'ZAR', 'size': value['size'], \
                         'sku_id': value['id'], 'out_of_stock': value['stock_status']})
        return skus

    def brand(self, response):
        return response.css('.product-name h1::text').extract_first()

    def url(self, response):
        return response.css('link[rel="canonical"]::attr(href)').extract_first()

    def product_name(self, response):
        return response.css('.product-name h1::text').extract_first()

    def description(self, response, name):
        product_description = []
        product_description.append(name)
        for description_sel in response.css('#product-attribute-specs-table tbody>tr'):
            product_description.append(':'.join(description_sel.css('th::text, td::text').extract()))
        return product_description
