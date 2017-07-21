# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DarazItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    SKU = scrapy.Field()
    Colour = scrapy.Field()
    Resolution = scrapy.Field()
    ProcessorType = scrapy.Field()
    OS = scrapy.Field()
    Connectivity = scrapy.Field()
    RAM = scrapy.Field()
    Brand = scrapy.Field()
    Speed = scrapy.Field()
    Ratings = scrapy.Field()
    DisplaySize = scrapy.Field()
    Storage = scrapy.Field()
    ShippingWeight = scrapy.Field()
    Title = scrapy.Field()
