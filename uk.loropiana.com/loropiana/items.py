# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LoropianaItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    trail = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    product_name = scrapy.Field()
    gender = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    url = scrapy.Field()
    skus = scrapy.Field()
