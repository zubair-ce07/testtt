# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EloquiiProduct(scrapy.Item):
    product_id = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    merch_info = scrapy.Field()
    out_of_stock = scrapy.Field()
