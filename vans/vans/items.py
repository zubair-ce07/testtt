# -*- coding: utf-8 -*-
import scrapy


class VansItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    composition = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    images_url = scrapy.Field()
    retailer_id = scrapy.Field()
    gender = scrapy.Field()


