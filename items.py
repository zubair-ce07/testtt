# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    skus = scrapy.Field()
    gender = scrapy.Field()
    brand = scrapy.Field()
    date = scrapy.Field()
