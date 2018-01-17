# -*- coding: utf-8 -*-
import scrapy


class SferaItem(scrapy.Item):
    title = scrapy.Field()
    categories = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    url_original = scrapy.Field()
    skus = scrapy.Field()
    trails = scrapy.Field()
    retailer_sku = scrapy.Field()
    brand = scrapy.Field()