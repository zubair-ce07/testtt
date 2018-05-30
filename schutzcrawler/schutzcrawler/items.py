# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    sku = scrapy.Field()
    trail = scrapy.Field()
    url = scrapy.Field()
    out_of_stock = scrapy.Field()