# -*- coding: utf-8 -*-
import scrapy


class WhistlesItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    product_sku = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()

