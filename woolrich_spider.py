import datetime
import json
import re
import scrapy
import time
from scrapy.link import Link
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule, Request
from w3lib.url import add_or_replace_parameter


class PaginationLinks():

    def extract_links(self, response):
        pagination_url = response.css('.search-result-content::attr(data-url)').extract_first()
        if not pagination_url:
            return []
        request_url = []
        page_limit = int(response.css('.search-result-content::attr(data-maxpage)').extract_first())
        product_limit = int(response.css('.search-result-content::attr(data-pagesize)').extract_first())
        for value in range(2, page_limit + 1):
            request_url.append(Link(add_or_replace_parameter(pagination_url, '&start=', str(product_limit * value))))
        return request_url     


class WoolrichSpider(CrawlSpider):
    name = 'woolrich_spider'
    allowed_domains = ['woolrich.eu']
    start_urls = ['http://www.woolrich.eu/en/gb/new-arrivals/new-men/men-spring-2018/WOCPS2656-GT02.html']
    allowed_url = r'.*/en/.*'
    rules = [Rule(LinkExtractor(allow=(allowed_url), restrict_css='.menu-category'),
                                callback='parse', follow=True),
             Rule(PaginationLinks(), callback='parse'),
             Rule(LinkExtractor(allow=(allowed_url), restrict_css='.product-name'),
                                callback='parse_product')]
    care = ['polyster', 'cotton', 'silk', 'fabric', 'wash']

    def parse(self, response):
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
        product['care'], product['description'] = self.raw_description(response)
        product['images'] = self.images(response)
        product['date'] = int(time.time())
        product['skus'] = []
        product['currency'] = "POUND"
        product['spider_name'] = self.name
        product['crawl_start_time'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        product['request_queue'] = self.color_requests(response, product)
        for request in self.request_handler(product):
            yield request

    def parse_size(self, response):
        response.meta['product']['skus'].append(self.skus(response))
        for request in self.request_handler(response.meta.get('product')):
            yield request 

    def parse_color(self, response):
        response.meta['product']['request_queue'].extend(self.size_requests(response, response.meta.get('product')))
        for request in self.request_handler(response.meta.get('product')):
            yield request

    def request_handler(self, product):
        if product['request_queue']:
            yield product['request_queue'].pop()
        else:
            del product['request_queue']
            yield product

    def color_requests(self, response, product):
        colors = response.css('.color>.selectable>a::attr(href)').extract()
        return [Request(color, meta={'product': product}, callback=self.parse_color) for color in colors]

    def size_requests(self, response, product):
        sizes = response.css('.size>.selectable>a::attr(href)').extract()
        return [Request(size, meta={'product': product}, callback=self.parse_size) for size in sizes]

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

    def raw_description(self, response):
        description = response.css('.description::text').extract_first()
        if not description:
            return [], []
        raw_descp = list(filter(str.strip, description.strip().split('.')))
        care = [descp for descp in raw_descp if any(care in descp for care in self.care)]
        descp = [descp for descp in raw_descp if not any(care in descp for care in self.care)]
        return care, descp

    def skus(self, response):
        size_info = response.css('.size>.selected>a::text').extract_first().strip()
        stock_info = response.css('.in-stock-msg::text').extract_first() or 'Out of Stock'
        color_name = response.css('.color>.selected>a>div::text').extract_first().strip()
        skus_id = color_name.replace(" ", "-").lower() + '_' + size_info.replace(" ", "-").lower()
        return  {'size': size_info,
                 'color': color_name,
                 'price': response.meta.get('product')['price'],
                 'currency': response.meta.get('product')['currency'],
                 'stock_status': stock_info,
                 'skus_id': skus_id}
