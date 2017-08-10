# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    retailer_id = scrapy.Field()
    brand = scrapy.Field()
    details = scrapy.Field()
    skus = scrapy.Field()
