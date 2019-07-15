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

    def parse(self, response):
        for item in json.loads(response.text)['items']:
            yield scrapy.Request(
                url='https://api.newyorker.de/csp/products/public/product'
                    '/matchingProducts?country=de&id=' +
                    str(item['id'])+'&variantId=001&limit=3',
                meta={'trail': response.request.url},
                callback=self.parse_product
            )
        for i in range(0, json.loads(response.text)['totalCount'], 24):
            yield scrapy.Request(
                url=w3lib.url.add_or_replace_parameter(response.request.url, "offset", str(i)),
                meta={'trail': response.request.url},
                callback=self.parse_pagination)
            yield scrapy.Request(
                url=w3lib.url.add_or_replace_parameter(response.request.url, "offset", str(i)),
                meta={'trail': response.request.url},
                callback=self.parse_pagination)

    def parse_pagination(self, response):
        for item in json.loads(response.text)['items']:
            yield scrapy.Request(
                url='https://api.newyorker.de/csp/products/public/product'
                    '/matchingProducts?country=de&id=' +
                    str(item['id'])+'&variantId=001&limit=3',
                meta={'trail': response.request.url},
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
                        images.append('https://nyimages.blob.core.windows.net/ny-public/'+image.get('key'))
                    skus.append(self.extract_skus(sku))
                    price = sku.get('original_price')
                    currency = sku.get('currency')
            product_types.append(NewyorkerItem(
                retailer_sku=variant['id'],
                market=variant['country'],
                url_original=response.url,
                url='https://www.newyorker.de/pt/products/?gender=MALE#/products/detail/'+variant["id"]+'/001',
                category=variant['maintenance_group'],
                description=variant['descriptions'],
                brand=variant['brand'],
                gender=variant['customer_group'],
                price=price,
                currency=currency,
                image_urls=images,
                spider_name='new_yorker',
                crawl_start_time=self.crawler.stats.get_stats()['start_time'].strftime("%Y-%m-%dT%H:%M:%s"),
                skus=skus,
                industry=None,
                trail=response.meta.get('trail')
            ))
        return product_types

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
