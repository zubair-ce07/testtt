import re
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from lindex.items import Product


# utility methods
def clean_list(data):
    temp = []
    for item in data:
        temp.append(item.strip())
    return list(filter(None, temp))


class LindeSpider(CrawlSpider):
    name = 'lindex'
    # allowed_domains = ['www.lindex.com/']
    start_urls = ['https://www.lindex.com/eu/women/tops/#!/page1/only']
    base_url = 'https://www.lindex.com'
    data_url = 'https://www.lindex.com/WebServices/ProductService.asmx/GetProductData'
    request_payload = {"productIdentifier": None, "colorId": None, "isMainProductCard": True, "nodeId": 0,
                       "primaryImageType": 0}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parses)

    # rules = (
    #     Rule(LinkExtractor(restrict_css='p.info a.productCardLink'), callback="parse_product"),)
    def parses(self, response):
        urls = response.css('p.info a.productCardLink::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url='{}{}'.format(self.base_url, url), callback=self.parse_product)

    def parse_product(self, response):
        product = Product()
        self.url(response, product)
        retailer_id = self.retailer_id(response, product)
        self.care(response, product)
        product['image_urls'] = []
        product['skus'] = {}
        currency = response.css('span.price')[0].css('::text').extract_first().strip()
        color_ids = response.css('ul.colors')[0].css('a::attr(data-colorid)').extract()
        self.request_payload.update({'productIdentifier': retailer_id, 'colorId': color_ids.pop()})
        print(self.request_payload)
        print(json.dumps(self.request_payload))
        yield scrapy.Request(url=self.data_url, method='POST', body=json.dumps(self.request_payload),
                             headers={'content-type': 'application/json'}, callback=self.parse_color,
                             meta={'product': product, 'currency': currency, 'color_ids': color_ids}, dont_filter=True)

    def parse_color(self, response):
        data = json.loads(response.body.decode("utf-8"))['d']
        product = response.meta.get('product')
        currency = response.meta.get('currency')
        color_ids = response.meta.get('color_ids')
        self.product_name(data, product)
        self.details(data, product)
        self.image_urls(data, product)
        self.skus(currency, data, product)
        if color_ids:
            self.request_payload.update({'colorId': color_ids.pop()})
            yield scrapy.Request(url=self.data_url, method='POST', body=json.dumps(self.request_payload),
                                 headers={'content-type': 'application/json'},
                                 callback=self.parse_color,
                                 meta={'product': product, 'currency': currency, 'color_ids': color_ids})
        else:
            yield product

    @staticmethod
    def retailer_id(response, product):
        product['retailer_id'] = response.css('p.product_id::text').extract()[-1].strip()
        return product['retailer_id']

    @staticmethod
    def url(response, product):
        product['url'] = response.url.split('?')[0]

    @staticmethod
    def care(response, product):
        product['care'] = clean_list(response.css('div.more_info ::text').extract())

    @staticmethod
    def product_name(data, product):
        product['name'] = data['Name']

    @staticmethod
    def details(data, product):
        product['details'] = clean_list(data['ProductFacts'])
        product['details'].append(re.sub(r'<.*?>', '', data['Description'].strip()))

    @staticmethod
    def image_urls(data, product):
        for image in data['Images']:
            product['image_urls'].append(image['XLarge'])

    @staticmethod
    def skus(currency, data, product):

        for i in range(1, len(data['SizeInfo'])):
            size_text = data['SizeInfo'][i]['Text']
            size_name = re.search(r'(?P<size>.+)\(', size_text)
            out_of_stock = False
            if size_name:
                size_name = size_name.group('size')
            else:
                size_name = re.search(r'(?P<size>.+)-', size_text)
                if size_name:
                    size_name = size_name.group('size')
                    out_of_stock = True
            product['skus'].update(
                {'{}_{}'.format(data['SKU'], size_name): {'size': size_name, 'currency': currency,
                                                          'sale_price': data['Price'],
                                                          'regular_price': data.get('NormalPrice', data['Price']),
                                                          'color': data['Color'], 'out_of_stock': out_of_stock}})
