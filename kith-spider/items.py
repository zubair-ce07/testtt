# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KithItem(scrapy.Item):
    # define the fields for your item here like:
    # define the fields for your item here like:
    name = scrapy.Field()
    colour = scrapy.Field()
    price = scrapy.Field()
    detail = scrapy.Field()
    sku_id = scrapy.Field()
    image_link = scrapy.Field()
    pass

