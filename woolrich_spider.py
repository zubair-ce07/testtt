import datetime
import json
import re
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule


class WoolrichSpider(CrawlSpider):
    name = 'woolrich_spider'
    allowed_domains = ['woolrich.eu']
    start_urls = ['http://www.woolrich.eu/en/gb/men/']
    allowed_url = r'.*/en/.*'
    rules = [Rule(LinkExtractor(allow=(allowed_url), restrict_css='.menu-category'),
                                callback='parse', follow=True),
             Rule(LinkExtractor(allow=(allowed_url), restrict_css='.product-name'),
                                callback='parse_product')]
    care = ['polyster', 'cotton', 'silk', 'fabric', 'wash']

    def parse(self, response):
        pagination = response.css('.search-result-content::attr(data-url)').extract_first()
        if pagination:
            pagination += '&start='
            page_limit = int(response.css('.search-result-content::attr(data-maxpage)').extract_first())
            product_limit = int(response.css('.search-result-content::attr(data-pagesize)').extract_first())
            for value in range(2,page_limit+1):
                request_url = pagination + str(product_limit * value)
                yield scrapy.Request(request_url, callback=self.parse)
        page_title = response.css('title::text').extract_first()
        trail = response.meta.get('trail') or []
        trail.append([page_title, response.url])
        for request in super().parse(response):    
            request.meta['trail'] = trail.copy()
            yield request

    def parse_product(self, response):
        product = {}
        raw_product = self.raw_products(response)
        product['retailer_sku'] = self.retailer_sku(raw_product)
        product['uuid'] = "null"
        product['language'] = "en"
        product['trail'] = response.meta.get('trail')
        product['url'] = response.url
        product['url_original'] = response.url
        product['name'] = self.product_name(raw_product)
        product['price'] = self.price(raw_product)
        product['brand'] = self.brand(raw_product)
        product['market'] = "GB"
        product['retailer'] = product['brand'] + '-' + product['language']
        product['category'] = self.category(raw_product)
        product['care'], product['description'] = self.description(response)
        product['images'] = self.images(response)
        product['date'] = int(time.time())
        product['skus'] = []
        product['currency'] = "POUND"
        product['spider_name'] = self.name
        product['crawl_start_time'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        product['request_queue'] = self.color_requests(response, product)
        
        if product['request_queue']:
            yield product['request_queue'].pop()
        else:
            del response.meta.get('product')['request_queue']
            yield product

    def brand(self, attributes):
        return attributes['brand']

    def retailer_sku(self, attributes):
        return attributes['id']

    def product_name(self, attributes):
        return attributes['name']

    def price(self, attributes):
        return attributes['price']

    def category(self, attributes):
        return attributes['category']

    def images(self, response):
        return response.css('.productthumbnail>picture>img::attr(src)').extract()
    
    def raw_products(self, response):
        product_description = re.findall("dataLayer.push.apply(.+?);", response.text, re.S)[0][12:-1]
        product_description = json.loads(product_description)
        return product_description[0]['ecommerce']['detail']['products'][0]

    def description(self, response):
        care_list = []
        descp_list = []
        description = response.css('.description::text').extract_first()
        if not description:
            return [], []
        description = list(filter(str.strip, description.strip().split('.')))
        for value in description:
            care_list.extend([value for care in self.care if care in value])
            if value not in care_list:
                descp_list.append(value)
        return care_list, descp_list

    def color_requests(self, response, product):
        colors_link = response.css('.color>.selectable>a::attr(href)').extract()
        requests = [scrapy.Request(value, meta={'product': product}, callback=self.parse_color)
                    for value in colors_link]
        return requests

    def parse_color(self, response):
        response.meta['product']['request_queue'] = self.size_requests(response, response.meta.get('product'))
        if response.meta.get('product')['request_queue']:
            yield response.meta['product']['request_queue'].pop()
        else:
            del response.meta.get('product')['request_queue']
            yield response.meta.get('product')

    def size_requests(self, response, product):
        request_queue = product['request_queue']
        sizes_links = response.css('.size>.selectable>a::attr(href)').extract()
        request_queue.extend([scrapy.Request(link, meta={'product': product}, callback=self.parse_size)
                              for link in sizes_links])
        return request_queue

    def parse_size(self, response):
        size_info = response.css('.size>.selected>a::text').extract_first().strip()
        stock_info = response.css('.in-stock-msg::text').extract_first() or 'Out of Stock'
        color_name = response.css('.color>.selected>a>div::text').extract_first().strip()
        skus_id = color_name.replace(" ", "-").lower() + '_' + size_info.replace(" ", "-").lower()
        response.meta['product']['skus'].append({'size': size_info,
                                                 'color': color_name,
                                                 'price': response.meta.get('product')['price'],
                                                 'currency': response.meta.get('product')['currency'],
                                                 'stock_status': stock_info,
                                                 'skus_id': skus_id}) 
        if response.meta.get('product')['request_queue']:
            yield response.meta.get('product')['request_queue'].pop()
        else:
            del response.meta.get('product')['request_queue']
            yield response.meta.get('product') 
