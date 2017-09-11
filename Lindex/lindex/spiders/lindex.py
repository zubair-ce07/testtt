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
    start_urls = ['https://www.lindex.com/m/eu/']
    base_url = 'https://www.lindex.com'
    data_url = 'https://www.lindex.com/WebServices/ProductService.asmx/GetProductData'
    pagination_url = 'https://www.lindex.com/eu/SiteV3/Category/GetProductGridPage'
    product_ids = []
    request_payload = {
        "productIdentifier": None,
        "colorId": None,
        "isMainProductCard": True,
        "nodeId": 0,
        "primaryImageType": 0
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.get_all_categories)

    def get_all_categories(self, response):
        categories = response.xpath('//nav/ul/li[@class="nonPage"]')[1:].xpath(
            'span/following-sibling::*[1][self::ul]/li/ul/li[1][not(./ul)]/a/@href').extract()[:-1]
        urls = []
        for category in categories:
            url = re.search(r'/m(?P<url>.+)', category).group('url')
            urls.append('{}{}'.format(self.base_url, url))
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_category)

    def parse_category(self, response):
        node_id = response.css('body::attr(data-page-id)').extract_first()
        formdata = {'nodeID': str(node_id), 'pageIndex': str(0)}
        return scrapy.FormRequest(self.pagination_url, formdata=formdata, callback=self.parse_page,
                                  meta={'formdata': formdata}, dont_filter=True)

    def parse_page(self, response):
        if response.css('p.info'):
            urls = ['{}{}'.format(self.base_url, url) for url in
                    response.css('p.info a.productCardLink::attr(href)').extract()]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_product)
            formdata = response.meta.get('formdata')
            formdata['pageIndex'] = str(int(formdata['pageIndex']) + 1)
            yield scrapy.FormRequest(self.pagination_url, formdata=formdata, callback=self.parse_page,
                                     meta={'formdata': formdata}, dont_filter=True)

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
        yield scrapy.Request(url=self.data_url, method='POST', body=json.dumps(self.request_payload),
                             headers={'content-type': 'application/json'}, callback=self.parse_color,
                             meta={'product': product, 'currency': currency, 'color_ids': color_ids, 'first': True})

    def parse_color(self, response):
        data = json.loads(response.body.decode("utf-8"))['d']
        product = response.meta.get('product')
        currency = response.meta.get('currency')
        color_ids = response.meta.get('color_ids')
        if response.meta.get('first'):
            self.product_name(data, product)
            self.details(data, product)
        self.image_urls(data, product)
        self.skus(currency, data, product)
        if color_ids:
            self.request_payload.update({"productIdentifier": product['retailer_id'], 'colorId': color_ids.pop()})
            yield scrapy.Request(url=self.data_url, method='POST', body=json.dumps(self.request_payload),
                                 headers={'content-type': 'application/json'}, callback=self.parse_color,
                                 meta={'product': product, 'currency': currency, 'color_ids': color_ids})
        elif product['retailer_id'] not in self.product_ids:
            self.product_ids.append(product['retailer_id'])
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

    def skus(self, currency, data, product):
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
                {'{}_{}'.format(data['SKU'], size_name): {'relative_url': self.base_url + data['RelativeGenericUrl'],
                                                          'size': size_name, 'currency': currency,
                                                          'sale_price': data['Price'],
                                                          'regular_price': data.get('NormalPrice', data['Price']),
                                                          'color': data['Color'], 'out_of_stock': out_of_stock}})
