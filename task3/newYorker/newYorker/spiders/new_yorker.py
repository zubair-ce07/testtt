# -*- coding: utf-8 -*-
import scrapy
import json
import w3lib.url
from newYorker.items import NewyorkerItem


class NewYorkerSpider(scrapy.Spider):
    name = 'new_yorker'
    allowed_domains = ['newyorker.de']
    start_urls = [
                  "https://api.newyorker.de/csp/products/public/query?"
                  "filters[country]=pt&filters[gender]=MALE&limit=24&offset=0",
                  "https://api.newyorker.de/csp/products/public/query?"
                  "filters[country]=pt&filters[gender]=FEMALE&limit=24&offset=0",
                  ]
    industry = None

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
            yield scrapy.Request(
                url=w3lib.url.add_or_replace_parameter(response.url, "offset", str(i)),
                meta={'trail': response.url},
                callback=self.parse_pagination)

    def parse_pagination(self, response):
        for item in json.loads(response.text)['items']:
            yield scrapy.Request(
                url=f'https://api.newyorker.de/csp/products/public/product'
                    f'/matchingProducts?country=de&id={str(item["id"])}&variantId=001&limit=3',
                meta={'trail': response.url},
                callback=self.parse_product
            )

    def parse_product(self, response):
        skus = []
        product_types = []
        for variant in json.loads(response.text):
            images = []
            for sku in variant.get('variants'):
                if sku:
                    for image in sku.get('images'):
                        images.append(f"https://nyimages.blob.core.windows.net/ny-public/{image.get('key')}")
                    skus.append(self.extract_skus(sku))
                    price = sku.get('original_price')
                    currency = sku.get('currency')
            product = self.boilerplate(NewyorkerItem(), response)
            product['retailer_sku'] = variant['id']
            product['market'] = variant['country']
            product['url'] = f'https://www.newyorker.de/pt/products/?gender=MALE#/products/detail/{variant["id"]}/001'
            product['category'] = variant['maintenance_group']
            product['description'] = variant['descriptions']
            product['brand'] = variant['brand']
            product['gender'] = variant['customer_group']
            product['price'] = price
            product['currency'] = currency
            product['image_urls'] = images
            product['skus'] = skus
            product_types.append(product)
        return product_types

    def boilerplate(self, product, response):
        product['spider_name'] = self.name
        product['industry'] = self.industry
        product['trail'] = response.meta.get('trail')
        product['url_original'] = response.url
        product['crawl_start_time'] = self.crawler.stats.get_stats()['start_time'].strftime("%Y-%m-%dT%H:%M:%s")
        return product

    def extract_skus(self, product_variant):
        skus = []
        for size in product_variant['sizes']:
            skus.append({
                'color': product_variant['basic_color'],
                'currency': product_variant['currency'],
                'price': product_variant['current_price'],
                'size': size.get('size_name')
            })
        return skus
