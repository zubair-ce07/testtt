# -*- coding: utf-8 -*-
import scrapy


class SheegoItem(scrapy.Item):
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    categories = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    total_rating = scrapy.Field()
    rating = scrapy.Field()
    details = scrapy.Field()
    description = scrapy.Field()
    materials = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()

