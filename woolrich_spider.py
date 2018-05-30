import datetime
import json
import queue
import re
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule


class WoolrichSpider(CrawlSpider):
    name = 'woolrich_spider'
    allowed_domains = ['woolrich.eu']
    start_urls = ['http://www.woolrich.eu/en/gb/home']
    rules = [Rule(LinkExtractor(allow=(r'.*/en/.*'), restrict_css='.menu-category'),
                                callback='parse', follow=True),
             Rule(LinkExtractor(allow=(r'.*/en/.*'), restrict_css='.product-name'),
                                callback='parse_product')]
    care = ['polyster', 'cotton', 'silk', 'fabric', 'wash']

    def parse(self, response):
        trail = response.meta.get('trail') or []
        for request in super().parse(response):
            page_title = response.css('title::text').extract_first()
            request.meta['trail'] = trail.copy()
            request.meta['trail'].append([page_title, response.url])
            yield request

    def parse_product(self, response):
        product = {}
        attributes = self.attributes(response)
        product['retailer_sku'] = self.retailer_sku(attributes)
        product['uuid'] = "null"
        product['language'] = "en"
        product['trail'] = response.meta.get('trail')
        product['url'] = response.url
        product['url_original'] = response.url
        product['name'] = self.product_name(attributes)
        product['price'] = self.price(attributes)
        product['brand'] = self.brand(attributes)
        product['language'] = self.language(attributes)
        product['market'] = self.market(attributes)
        product['retailer'] = product['brand'] + '-' + product['language']
        product['category'] = self.category(attributes)
        product['care'] = []
        product['description'] = []
        self.description(response, product['care'], product['description'])
        product['images'] = self.images(response)
        product['date'] = int(time.time())
        product['skus'] = []
        product['currency'] = 'POUND'
        product['request_queue'] = queue.Queue()
        product['spider_name'] = "woolrich_spider"
        product['crawl_start_time'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        colors_name = response.css('.swatch::text').extract()
        colors_link = response.css('.color>.selectable>a::attr(href)').extract()
        for index, value in enumerate(colors_link):
            request = scrapy.Request(value, meta={'color': colors_name[index].strip(), 'product': product},
                                     callback=self.sizes)
            product['request_queue'].put(request)

        yield product['request_queue'].get(request)

    def attributes(self, response):
        product_description = re.findall("dataLayer.push.apply(.+?);", response.text, re.S)[0][12:-1]
        return json.loads(product_description)

    def description(self, response, care_list, descp_list):
        description = response.css('.description::text').extract_first()
        if not description:
            return
        description = list(filter(str.strip, description.strip().split('.')))
        for value in description:
            care_list.extend([value for care in self.care if care in value])
            if value not in care_list:
                descp_list.append(value)

    def market(self, attributes):
        return attributes[1]['country'].upper()

    def language(self, attributes):
        return attributes[1]['language']

    def brand(self, attributes):
        return attributes[0]['ecommerce']['detail']['products'][0]['brand']

    def retailer_sku(self, attributes):
        return attributes[0]['ecommerce']['detail']['products'][0]['id']

    def product_name(self, attributes):
        return attributes[0]['ecommerce']['detail']['products'][0]['name']

    def price(self, attributes):
        return attributes[0]['ecommerce']['detail']['products'][0]['price']

    def category(self, attributes):
        return attributes[0]['ecommerce']['detail']['products'][0]['category']

    def images(self, response):
        return response.css('.productthumbnail>picture>img::attr(src)').extract()

    def sizes(self, response):
        sizes_links = response.css('.size>.selectable>a::attr(href)').extract()
        for link in sizes_links:
            request = scrapy.Request(link, meta={'color': response.meta.get('color'),
                                                 'product': response.meta.get('product')},
                                                  callback=self.skus_maker)
            response.meta['product']['request_queue'].put(request)
        yield response.meta.get('product')['request_queue'].get()

    def skus_maker(self, response):
        size_info = response.css('.size>.selected>a::text').extract_first().strip()
        stock_info = response.css('.in-stock-msg::text').extract_first() or 'Out of Stock'
        skus_id = response.meta.get('color').replace(" ", "-").lower() + '_' + size_info.replace(" ","-").lower()
        response.meta['product']['skus'].append({'size': size_info,
                                                 'color': response.meta.get('color'),
                                                 'price': response.meta.get('product')['price'],
                                                 'currency': response.meta.get('product')['currency'],
                                                 'stock_status': stock_info,
                                                 'skus_id': skus_id}) 
        if response.meta.get('product')['request_queue'].qsize() > 0:
            yield response.meta.get('product')['request_queue'].get()
        else:
            del response.meta.get('product')['request_queue']
            yield response.meta.get('product') 
