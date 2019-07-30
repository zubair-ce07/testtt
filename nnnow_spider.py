import scrapy
import json

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
        item['skus'] = []
        item['category'] = self.get_category(response)
        item['image_urls'] = self.get_image_urls(response)
        item['url'] = self.get_url(response)
        item['description'] = self.get_description(converted_data)
        item['care'] = self.get_care(converted_data)
        item['requests'] = []
        item['requests'].extend(self.color_requests(converted_data, item))
        return self.get_request_or_item(item)

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

    def color_requests(self, converted_data, item):
        color_ids = []
        one_color_data = converted_data['ProductStore']['PdpData']['mainStyle']['styleId']
        if converted_data.get('ProductStore', {}).get('PdpData', {}).get('colors', {}).get('colors', {}).get('', {}):
            multiple_colors_data = converted_data['ProductStore']['PdpData']['colors']['colors']['']
            for color in multiple_colors_data:
                color_ids.append(color['styleId'])
        else:
            color_ids.append(one_color_data)
        headers = {
            'Origin': 'https://www.nnnow.com',
            'Content-Type': 'application/json',
            'module': 'odin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
        url = 'https://api.nnnow.com/d/api/product/details'
        for ids in color_ids:
            data = {"module": "odin", "styleId": ""}
            data['styleId'] = ids
            requests_all = []
            requests_all.append(
                scrapy.Request(url=url, method="POST", headers=headers, meta={"item": item}, callback=self.parse_colors, body=json.dumps(data)))
        return requests_all

    def get_request_or_item(self, item):
        if item['requests']:
            return item['requests'].pop()
        del item["requests"]
        return item

    def parse_colors(self, response):
        item = response.meta["item"]
        responses = json.loads(response.body)
        color = responses['data']['mainStyle']['colorDetails']['primaryColor']
        skus_all = responses['data']['mainStyle']['skus']
        sku_list = []
        for one_sku in skus_all:
            if one_sku['inStock'] == 'False':
                out_of_stock = 'True'
            else:
                out_of_stock = 'False'
            sku = {'Size': one_sku['size'], 'skuId': one_sku['skuId'], 'price': one_sku['price'], 'out_of_stock': out_of_stock}
            sku_list.append(sku)
            all_skus = {'color': color, 'skus': sku_list}
            item['skus'] = all_skus
        return self.get_request_or_item(item)

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
    skus = scrapy.Field()
    url = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    requests = scrapy.Field()
