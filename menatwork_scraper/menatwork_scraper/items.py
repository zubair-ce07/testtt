# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    name = scrapy.Field()
    colors = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    currency = scrapy.Field()
    image_url = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    gender = scrapy.Field()
