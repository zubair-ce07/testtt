# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()

    price = scrapy.Field()
    currency = scrapy.Field()
    sizes = scrapy.Field()
    colors = scrapy.Field()

    image_urls = scrapy.Field()
    care = scrapy.Field()
    id = scrapy.Field()
