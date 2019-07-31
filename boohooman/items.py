# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    # define the fields for your item here like:
    product_code = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_description = scrapy.Field()
    product_category = scrapy.Field()
    product_link = scrapy.Field()
    data_skus = scrapy.Field()


class ProductSkus(scrapy.Item):
    color = scrapy.Field()
    sizes = scrapy.Field()
    pictures = scrapy.Field()
