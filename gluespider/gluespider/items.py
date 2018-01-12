# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GluesProduct(scrapy.Item):
    brand = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    remaining_request = scrapy.Field()
    information = scrapy.Field()
