# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstscrapytaskItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductInfo(scrapy.Item):

    name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    product_code = scrapy.Field()
    price_final = scrapy.Field()
    desc = scrapy.Field()
    color = scrapy.Field()
    currency = scrapy.Field()
    image_urls = scrapy.Field()
    sizes_info = scrapy.Field()
