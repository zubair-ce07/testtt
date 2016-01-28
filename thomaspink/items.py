# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThomaspinkItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    availability = scrapy.Field()
