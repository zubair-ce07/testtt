# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AsicsItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    original_url = scrapy.Field()
    image_urls = scrapy.Field()
    brand = scrapy.Field()
    currency = scrapy.Field()
    lang = scrapy.Field()
    gender = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
    date = scrapy.Field()
    merch_info = scrapy.Field(default=[])
    trail: scrapy.Field(default=None)
    uuid: scrapy.Field(default=None)
    retailer: scrapy.Field(default='asics-us')
    market: scrapy.Field(default='US')
