# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VeromodaSpiderItem(scrapy.Item):

    # define the fields for your item here like:
    category = scrapy.Field()
    product_id = scrapy.Field()
    description = scrapy.Field()
    url_orignal = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()


class skuItem(scrapy.Item):

    currency = scrapy.Field()
    price = scrapy.Field()
    out_of_stock = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()


