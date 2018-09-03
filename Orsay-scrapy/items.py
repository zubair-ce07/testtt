# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OrsayItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    categories = scrapy.Field()
    care = scrapy.Field()
    details = scrapy.Field()
    images = scrapy.Field()
    item_url = scrapy.Field()
    sizes = scrapy.Field()
    retail_sku = scrapy.Field()
    skus = scrapy.Field()


class SizeInfo(scrapy.Item):
    colors = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    size = scrapy.Field()
    in_stock = scrapy.Field()