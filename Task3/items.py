# -*- coding: utf-8 -*-
import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    lang = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()



