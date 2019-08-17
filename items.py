# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ClothesItem(scrapy.Item):
    url = scrapy.Field()
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    skus = scrapy.Field()
    requests = scrapy.Field()
