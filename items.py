# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JelmoliItem(scrapy.Item):
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    industry = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    lang = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
