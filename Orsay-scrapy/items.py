# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OrsayItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    url = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    brand = scrapy.Field()
    gender = scrapy.Field()


class SizeInfo(scrapy.Item):
    colour = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    size = scrapy.Field()
    out_of_stock = scrapy.Field()

