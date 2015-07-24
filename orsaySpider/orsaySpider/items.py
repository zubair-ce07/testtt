# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class linksItem(scrapy.Item):
    link= scrapy.Field()

class skuItem(scrapy.Item):
    currency = scrapy.Field()
    price = scrapy.Field()
    previous_prices = scrapy.Field()
    colour = scrapy.Field()
    size = scrapy.Field()

class orsayItem(scrapy.Item):
    # define the fields for your item here like:
    currency = scrapy.Field()
    category = scrapy.Field()
    retailer_sku = scrapy.Field()
    description = scrapy.Field()
    url_orignal = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
    lang = scrapy.Field()
    name = scrapy.Field()