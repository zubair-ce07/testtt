import scrapy
from scrapy.spiders import Spider

import json

from ..items import AmiparisItem


class BeginningBoutique(Spider):
    name = "amiparis"
    market = 'us'
    retailer = 'amiparis-us'
    base_url = 'https://www.amiparis.com/us/'
    start_urls = ['https://www.amiparis.com/us/']
    prouduct_url_format = "{}/shopping/{}?StoreId={}?gender={}"
    nav_url_format = "{}api{}"
    skus_url_format = "{}/shopping/{}"

    def parse(self, response):
        nav_list = response.css('.navSub-ul li>a::attr(href)').extract()
        for nav in nav_list:
            yield scrapy.Request(self.nav_url_format.format(self.base_url, nav[3:]), method='GET',
                                 headers={'Content-Type': 'application/json'},
                                 callback=self.parse_categories)

    def parse_categories(self, response):
        category_body = json.loads(response.body)
        category_entries = category_body['products']['entries']
        for entry in category_entries:
            entry['slug'] = self.prouduct_url_format.format(self.base_url, entry['slug'], str(entry['merchantId']),
                                                            str(entry['gender']))
            yield scrapy.Request(entry['slug'], callback=self.parse_product)

    def parse_product(self, response):
        item = self.extract_product(response)
        skus_urls = []
        colors_urls = response.css('.color__list  a::attr(href)').extract()
        for color_url in colors_urls:
            skus_urls.append(
                scrapy.Request(self.skus_url_format.format(self.base_url, color_url.split('/')[-1]),
                               callback=self.parse_items))

        yield self.next_request_or_product(skus_urls, item)

    def next_request_or_product(self, skus_urls, item):
        if len(skus_urls) == 0:
            return item
        else:
            req = skus_urls.pop()
            req.meta['item'] = item
            req.meta['req_urls'] = skus_urls
            return req

    def parse_items(self, response):
        item = response.meta['item']
        sizes = response.css('.size__list a::text').getall()
        colour = response.css('a.color__link--isActive::attr(data-tooltip)').get()
        for size in sizes:
            if colour + '_' + size in item['skus'].keys():
                item['skus'][colour + '_' + size].append({'size': size, 'colour': colour, 'price': item['price'],
                                                          'currency': item['currency']})
            else:
                item['skus'][colour + '_' + size] = {'size': size, 'colour': colour, 'price': item['price'],
                                                     'currency': item['currency']}

        yield self.next_request_or_product(response.meta['req_urls'], item)

    def extract_product(self, response):
        item = AmiparisItem()
        item['name'] = response.css('.product-title::text').get()
        item['gender'] = 'Women'
        item['currency'] = response.css('.js-location-btn span:nth-child(2)::text').get()
        item['url_original'] = response.url
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['skus'] = dict()
        item['brand'] = response.css('.product-scale-description::text').get()
        item['price'] = response.css('.product-price::text').get()[2:]
        item['image_urls'] = response.css('.swiper-wrapper')[0].xpath(".//img/@src").getall()
        item['description'] = response.css('#product_information_Advices ::text').getall()
        item['care'] = response.css('#product_information_CareGuide li::text').getall()
        item['category'] = response.css('.breadcrumb-item span::text').getall()
        return item
