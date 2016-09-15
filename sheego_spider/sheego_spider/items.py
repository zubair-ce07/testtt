# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SheegoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    care = scrapy.Field()
    gender = scrapy.Field()
    url_original = scrapy.Field()
    pid = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    skus = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
