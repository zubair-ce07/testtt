# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import requests
import json


class WoolworthSpider(CrawlSpider):
    name = 'woolworths'
    allowed_domains = ['woolworths.co.za']
    start_urls = ['https://woolworths.co.za']

    rules = (
        Rule(LinkExtractor(restrict_css='li.main-nav__list-item--primary > ul:nth-child(2) > li > a', strip=True),
             callback='parse_main_products'),
    )

    def parse_main_products(self, response):
        product_links = self.product_link(response)
        for product in product_links:
            yield scrapy.http.Request(product, callback=self.parse_products)

        pagination_pages = self.pagination_links(response)
        for page in pagination_pages:
            yield scrapy.http.Request(page, callback=self.parse_main_products)

    def parse_products(self, response):
        resp = response.css('body > script::text')[0].extract()
        json_resp = json.loads(resp.split('= ')[1])
        item = {
            'description': self.description(response),
            'type': self.product_type(json_resp),
            'image_url': self.image_url(json_resp),
            'product_name': self.product_name(response),
            'sku': self.sku_id(response),
            'url': response.url,
            'skus': self.populate_sku_for_all_sizes(json_resp, response)
        }
        yield item

    def populate_sku_for_all_sizes(self, json_resp, response):
        items = {
            'skus': {}
        }
        price = self.price(response)
        for col in self.colors(json_resp):
            for idx, size in enumerate(self.sizes(json_resp)):
                values = {
                    'color': col,
                    'currency': 'ZAR',
                    'price': price,
                    'size': size
                }
                items['skus']['{0}_{1}_{2}'.format(self.sku_id(response), size, col)] = values
            return items['skus']

    def product_type(self, response):
        prod_type = (response['pdp']['productInfo']['breadcrumbs']['default'])
        return [d[k] for d in prod_type for k in d if k == 'label']

    def colors(self, response):
        color = (response['pdp']['productInfo']['colourSKUs'])
        return [d[k] for d in color for k in d if k == 'colour']

    def price(self, response):
        price_url = 'http://www.woolworths.co.za/server/getProductPrice?productIds=' + str(self.sku_id(response))
        resp = requests.post(price_url)
        return resp.json()[self.sku_id(response)]['plist3620008']['priceMax']

    def pagination_links(self, response):
        pagination_pages = response.css('.pagination > a::attr(href)').extract()
        return [response.urljoin(page) for page in pagination_pages]

    def product_link(self, response):
        product_links = response.css('div.product-list__item > article:nth-child(1) > div:nth-child(1) > '
                                     'a:nth-child(1)::attr(href)').extract()
        return [response.urljoin(prod) for prod in product_links]

    def sizes(self, response):
        size = (response['pdp']['productInfo']['styleIdSizeSKUsMap']).values()[0]
        return [d[k] for d in size for k in d if k == 'size']

    def image_url(self, response):
        url = (response['pdp']['productInfo']['colourSKUs'])
        image_url = [d[k] for d in url for k in d if k == 'externalImageUrlReference']
        return ['https://woolworths.co.za/{0}'.format(image) for image in image_url]

    def description(self, response):
        return ' '.join(t.strip() for t in response.css('div.accordion__segment--chrome:nth-child(1) '
                                                        '> div ::text').extract()[:-2]).strip()

    def sku_id(self, response):
        return response.css('ul.list--silent > li:nth-child(2)::text').extract()[0]

    def product_name(self, response):
        return response.css('h1.font-graphic::text').extract()
