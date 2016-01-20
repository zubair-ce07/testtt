# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoccinelleItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    retailer_sku = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    price = scrapy.Field()
    colours = scrapy.Field()
    pass
