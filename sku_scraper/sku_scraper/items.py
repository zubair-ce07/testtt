# -*- coding: utf-8 -*-

import scrapy


class Item(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()
    url = scrapy.Field()
    meta = scrapy.Field()
    merch_info = scrapy.Field()
