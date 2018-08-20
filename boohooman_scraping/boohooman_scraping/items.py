# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    brand = scrapy.Field()
    category = scrapy.Field(serializer=list)
    currency = scrapy.Field()
    description = scrapy.Field()
    merch_info = scrapy.Field(serializer=list)
    name = scrapy.Field()
    price = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field(serializer=dict)
    image_urls = scrapy.Field(serializer=list)
    url = scrapy.Field()


class ProductSku(scrapy.Item):
    color = scrapy.Field()
    currency = scrapy.Field()
    original_price = scrapy.Field()
    discounted_price = scrapy.Field()
    size = scrapy.Field()