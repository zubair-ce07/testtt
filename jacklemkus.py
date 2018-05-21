import scrapy
import json
import time
import datetime
import re
from ast import literal_eval
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

class JacklemkusSpider(CrawlSpider):
    crawl_start_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    name = 'jacklemkus'
    allowed_domains = ['jacklemkus.com']
    start_urls = ['https://www.jacklemkus.com/']

    rules = (
             Rule(LinkExtractor(), callback='parse_products', follow=True),
            )

    def parse_products(self, response):
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        selector = Selector(response)
        product = response.xpath('//*[@class="sku"]/text()').extract_first()

        if not product:
            return

        product = {
                    'retailer_sku': '',
                    'uuid': 'null',
                    'trail': '',
                    'gender': '',
                    'category': '',
                    'industry': 'null',
                    'brand': '',
                    'url': '',
                    'date': '',
                    'url_original': '',
                    'name': '',
                    'description': '',
                    'care': '[]',
                    'image_urls': [],
                    'skus': [],
                    'price': '',
                    'currency': 'ZAR',
                    'spider_name': 'jacklemkus',
                    'crawl_start_time': self.crawl_start_time
                   }

        product_description = []
        trail_redirections = response.xpath('//*[@class="breadcrumbs"]/ul/li/a/text()').extract()
        breadcrum_urls = response.xpath('//*[@class="breadcrumbs"]/ul/li/a/@href').extract()

        product['retailer_sku'] = response.xpath('//*[@class="sku"]/text()').extract_first()
        product['category'] = selector.css('[class="breadcrumbs"]>ul>li:nth-child(2)>a::text').extract_first()
        product['trail'] = list(zip(trail_redirections, breadcrum_urls))
        product['brand'] = response.xpath('//*[@class="product-name"]/h1/text()').extract_first()
        product['url'] = selector.css('link[rel="canonical"]::attr(href)').extract_first()
        product['date'] = time.time()
        product['url_original'] = response.url
        product['name'] = response.xpath('//*[@class="product-name"]/h1/text()').extract_first()
        product_details = selector.css('td:last-child::text').extract()
        product['gender'] = product_details[0]
        product_attributes = selector.css('th:first-child::text').extract()
        product_price = re.findall("var optionsPrice = new Product.OptionsPrice(.+?);\n", response.body.decode('utf-8'), re.S)
        price_details = json.loads(product_price[0][1:-1])
        product_description.append(product['name'])

        for index, value in enumerate(product_details):
            product_description.append(product_attributes[index])
            product_description.append(product_details[index])

        product['description'] = product_description
        product['image_urls'] = response.xpath('//*[@class="hidden-xs"]/a/img/@src').extract()
        product['skus'] = self.product_skus(response, price_details['productPrice'])
        product['price'] = price_details['productPrice']

        yield product

    def product_skus(self, response, product_price):
        skus = []
        product_details = response.xpath('//*[@class="product-data-mine"]/@data-lookup').extract_first()
        product_details = literal_eval(product_details)
        for index, value in product_details.items():
            skus.append({'price': product_price, 'currency': 'ZAR', 'size': value['size'], \
                         'sku_id': value['id'],'out_of_stock': value['stock_status']})
        return skus
