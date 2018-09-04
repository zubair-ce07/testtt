# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OrsayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Product(scrapy.Item):
    brand = 'Orsay'
    gender = 'women'
    name = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
    category = scrapy.Field()
    # care image url
    skus = scrapy.Field(serializer=dict)
    url = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()


class Sku(scrapy.Item):
    color = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
