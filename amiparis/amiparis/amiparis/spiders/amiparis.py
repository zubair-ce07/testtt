import scrapy
from scrapy.spiders import CrawlSpider

import json

from ..items import AmiparisItem


class BeginningBoutique(CrawlSpider):
    name = "amiparis"
    market = 'us'
    retailer = 'amiparis-us'
    base_url = 'https://www.amiparis.com/'
    start_urls = ['https://www.amiparis.com/us/']
    request_urls = []

    def parse(self, response):
        nav_list = response.css('.navSub-ul li>a::attr(href)').extract()
        for nav in nav_list:
            yield scrapy.Request(self.base_url + 'api' + nav[3:], method='GET',
                                 headers={'Content-Type': 'application/json'},
                                 callback=self.parse_categories)

    def parse_categories(self, response):
        body = json.loads(response.body)
        for entry in body['products']['entries']:
            entry['slug'] = self.base_url + 'us/shopping/' + entry['slug'] + '?StoreId=' + str(
                entry['merchantId']) + '?gender=' + str(entry['gender'])
            yield scrapy.Request(entry['slug'], callback=self.parse_product)

    def parse_product(self, response):
        item = self.extract_product(response)
        items_urls = response.css('.color__list  a::attr(href)').extract()
        for item_url in items_urls:
            self.request_urls.append(
                scrapy.Request(self.base_url + item_url, callback=self.parse_items))

        req = self.request_urls.pop()
        req.meta['item'] = item
        yield req

    def next_request_or_product(self, items_urls, item):
        if len(items_urls) == 0:
            return item
        else:
            req = items_urls.pop()
            req.meta['item'] = item
            return req

    def parse_items(self, response):
        skus = []
        item = response.meta['item']
        sizes = response.css('.size__list a::text').getall()
        colour = response.css('a.color__link--isActive::attr(data-tooltip)').get()
        for size in sizes:
            skus.append({'size': size, 'colour': colour, 'price': item['price'], 'currency': item['currency']})

        item['skus'] = skus
        yield self.next_request_or_product(self.request_urls, item)

    def extract_product(self, response):
        item = AmiparisItem()
        item['name'] = response.css('.product-title::text').get()
        item['gender'] = 'Women'
        item['currency'] = response.css('.js-location-btn span:nth-child(2)::text').get()
        item['url_original'] = response.url
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['brand'] = response.css('.product-scale-description::text').get()
        item['price'] = response.css('.product-price::text').get()[2:]
        item['image_urls'] = response.css('.swiper-wrapper')[0].xpath(".//img/@src").getall()
        item['description'] = response.css('#product_information_Advices ::text').getall()
        item['care'] = response.css('#product_information_CareGuide li::text').getall()
        item['category'] = response.css('.breadcrumb-item span::text').getall()
        return item
