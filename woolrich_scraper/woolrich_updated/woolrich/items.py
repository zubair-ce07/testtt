# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WoolrichItem(scrapy.Item):
    name = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    style = scrapy.Field()
    path = scrapy.Field()
    image = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    pass
