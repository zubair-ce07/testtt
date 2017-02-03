#!/usr/bin/python2.7

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawler1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # field1 = scrapy.Field()
    # field2 = scrapy.Field()

    spider_name = scrapy.Field()
    retailer = scrapy.Field()
    currency = scrapy.Field()
    market = scrapy.Field()
    category = scrapy.Field()
    uuid = scrapy.Field()
    retailer_sku = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    # {
    # currency = scrapy.Field()
    # colour = scrapy.Field()
    # price = scrapy.Field()
    # size = scrapy.Field()
    # }
    care = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    gender = scrapy.Field()
    # field3 = scrapy.Field()
    # field4 = scrapy.Field()
    # field5 = scrapy.Field()
    # field6 = scrapy.Field()
    # pass
