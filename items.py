# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlueflyItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    care = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    merch_info = scrapy.Field()
    retailer = scrapy.Field()
    skus = scrapy.Field()
    retailer_sku = scrapy.Field()
    url = scrapy.Field()
    url_original = scrapy.Field()
