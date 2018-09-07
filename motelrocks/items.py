# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MotelItem(scrapy.Item):
    brand = scrapy.Field()
    category = scrapy.Field()
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    img_urls = scrapy.Field()
    url = scrapy.Field()
    skus = scrapy.Field()
    gender = scrapy.Field()
