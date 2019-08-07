# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BognerItem(scrapy.Item):
    url = scrapy.Field()
    retailer_sku = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    retailer = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
