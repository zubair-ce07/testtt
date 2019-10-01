# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductsItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    currency = scrapy.Field()
    market = scrapy.Field()
    image_urls = scrapy.Field()
    url_original = scrapy.Field()
    retailer = scrapy.Field()
    description = scrapy.Field()
