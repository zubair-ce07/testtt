# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SnkrsItem(scrapy.Item):
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    lang = scrapy.Field()
    trail = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    retailer = scrapy.Field()
    url_original = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()


class SnkrsSkuItem(scrapy.Item):
    colour = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    size = scrapy.Field()
    size_type = scrapy.Field()
    sku_id = scrapy.Field()
