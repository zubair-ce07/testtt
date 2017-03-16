# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MenatworkItem(scrapy.Item):
    brand = scrapy.Field()
    url = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    industry = scrapy.Field()
    market = scrapy.Field()
    merch_info = scrapy.Field()
    name = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field() 
    skus = scrapy.Field()
