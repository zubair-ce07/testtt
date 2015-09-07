# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    product_id = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    merch_info = scrapy.Field()


class SkuItem(scrapy.Item):
    currency = scrapy.Field()
    price = scrapy.Field()
    previous_prices = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    out_of_stock = scrapy.Field()
