# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GymboreeItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    category = scrapy.Field()
    currency = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    spider_name = scrapy.Field()
    trail = scrapy.Field()
    url = scrapy.Field()


class SKUS (scrapy.Item):
    colour = scrapy.Field()
    currency = scrapy.Field()
    out_of_stock = scrapy.Field()
    previous_price = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()