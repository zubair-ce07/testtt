# -*- coding: utf-8 -*-
import json
import w3lib.url

import scrapy

from newYorker.items import NewyorkerItem


class NewYorkerSpider(scrapy.Spider):
    name = 'new_yorker'
    allowed_domains = ['newyorker.de']
    start_urls = \
        [
          "https://api.newyorker.de/csp/products/public/query?filters[country]=pt"
          "&filters[gender]=MALE&limit=24&offset=0",

          "https://api.newyorker.de/csp/products/public/query?filters[country]=pt"
          "&filters[gender]=FEMALE&limit=24&offset=0",
        ]
    industry = None
    market = "PT"
    care = None
    retailer = 'newyorker.de'

    def parse(self, response):
        for item in json.loads(response.text)['items']:
            yield scrapy.Request(
                url=f'https://api.newyorker.de/csp/products/public/product'
                f'/matchingProducts?country=de&id={str(item["id"])}&variantId=001&limit=3',
                meta={'trail': response.url},
                callback=self.parse_product
            )
        for i in range(0, json.loads(response.text)['totalCount'], 24):
            yield scrapy.Request(
                url=w3lib.url.add_or_replace_parameter(response.url, "offset", str(i)),
                meta={'trail': response.url},
                callback=self.parse_pagination)

    def parse_pagination(self, response):
        for product in json.loads(response.text)['items']:
            yield self.parse_product(product, response)

    def parse_product(self, raw_product, response):
        product = self.boilerplate(NewyorkerItem(), response)
        product['retailer_sku'] = raw_product['id']
        product['name'] = raw_product['maintenance_group']
        product['category'] = raw_product['web_category']
        product['description'] = raw_product['descriptions']
        product['brand'] = raw_product['brand']
        product['gender'] = raw_product['customer_group']
        product['price'] = self.price(raw_product['variants'][0])
        product['currency'] = self.currency(raw_product['variants'][0])
        product['image_urls'] = self.images(raw_product['variants'][0])
        product['skus'] = self.extract_skus(raw_product)
        product['care'] = self.care
        return product

    def boilerplate(self, product, response):
        product['spider_name'] = self.name
        product['industry'] = self.industry
        product['market'] = self.market
        product['trail'] = response.meta.get('trail')
        product['url_original'] = response.url
        product['url'] = response.url
        product['retailer'] = self.retailer
        product['crawl_start_time'] = self.crawler.stats.get_stats()['start_time'].strftime("%Y-%m-%dT%H:%M:%s")
        return product

    def price(self, variant):
        return variant['original_price']

    def currency(self, variant):
        return variant['currency']

    def images(self, variant):
        images = []
        for image in variant['images']:
            images.append(f"https://nyimages.blob.core.windows.net/ny-public/{image.get('key')}")
        return images

    def extract_skus(self, raw_product):
        skus = {}
        color = raw_product['variants'][0].get('basic_color')
        currency = raw_product['variants'][0].get('currency')
        price = raw_product['variants'][0].get('current_price')
        for size in raw_product['variants'][0]['sizes']:
            skus[f'{raw_product["maintenance_group"]} - {size.get("size_name")} - {color}'] = {
                'colour': color,
                'currency': currency,
                'price': price,
                'size': size.get('size_name')
            }
        return skus
