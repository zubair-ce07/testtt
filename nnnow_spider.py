import scrapy
import json
import requests

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Nnnow(CrawlSpider):

    name = 'Nnnowspider'
    start_urls = ['https://www.nnnow.com/']
    all_products_paths = '/men', '/women', '/kids', '/footwear'
    product_css = '.nwc-grid-col .nw-productlist '

    rules = (
        Rule(LinkExtractor(allow=all_products_paths)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        converted_data = self.get_all_data(response)
        item = NnnowRecord()
        item['name'] = self.get_name(response)
        item['brand'] = self.get_brand(response)
        item['category'] = self.get_category(response)
        item['image_urls'] = self.get_image_urls(response)
        item['url'] = self.get_url(response)
        item['description'] =self.get_description(converted_data)
        item['care'] = self.get_care(converted_data)
        item['skus'] = self.get_skus(converted_data)
        return item

    def get_name(self, response):
        return response.css('.nw-product-name .nw-product-title::text').get()

    def get_brand(self, response):
        return response.css('.nw-product-name .nw-product-brandtxt::text').get()

    def get_category(self, response):
        return response.css('.nw-breadcrumblist-list .nw-breadcrumb-listitem::text').getall()

    def get_image_urls(self, response):
        return response.css('.nw-maincarousel-wrapper img::attr(src)').getall()

    def get_currency(self, response):
        return response.css('.nw-sizeblock-container  span::attr(content)').get()

    def get_all_data(self, response):
        all_data = response.xpath('//script[contains(text(), "specs")]/text()').re_first("DATA= (.+)")
        converted_data = json.loads(all_data)
        return converted_data

    def get_skus(self, converted_data):
        urls = converted_data['ProductStore']['PdpData']['colors']['colors']['']
        color_ids = []
        for item in urls:
            one_url = item['url']
            split_url = one_url.split("-")[-1]
            color_ids.append(split_url)
        return self.color_requests(color_ids)

    def color_requests(self, color_ids):
        headers = {
            'Origin': 'https://www.nnnow.com',
            'Content-Type': 'application/json',
            'module': 'odin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
        for item in color_ids:
            data = {"module":"odin","styleId":""}
            data['styleId'] = item
            response = requests.post('https://api.nnnow.com/d/api/product/details', headers=headers, data=json.dumps(data))
            return self.generate_skus(response)

    def generate_skus(self, response):
        skus_result = response.json()['data']['mainStyle']['skus']
        color_result = response.json()['data']['colors']['selectedColor']['primaryColor']
        sku_list = []
        for item in skus_result:
            if item['inStock'] == 'False':
                out_of_stock = 'True'
            else:
                out_of_stock = 'False'
            sku = (dict(
                {'Size': item['size'], 'skuId': item['skuId'], 'price': item['price'], 'out_of_stock': out_of_stock}))
            sku_list.append(sku)
            all_skus = dict({'color': color_result, 'skus': sku_list})
        return all_skus

    def get_url(self, response):
        return response.css("meta[name='og_url']::attr(content)").get()

    def get_care(self, converted_data):
        return converted_data['ProductStore']['PdpData']['mainStyle']['finerDetails']['compositionAndCare']['list']

    def get_description(self, converted_data):
        return converted_data['ProductStore']['PdpData']['mainStyle']['finerDetails']['specs']['list']


class NnnowRecord(scrapy.Item):

    name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    currency = scrapy.Field()
    skus= scrapy.Field()
    url = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
