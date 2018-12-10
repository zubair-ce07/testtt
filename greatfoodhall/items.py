# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GreatfoodhallItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    category = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    type_weight = scrapy.Field()
    nutrition = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    url = scrapy.Field()
    pass
