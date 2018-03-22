# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductData(scrapy.Item):
    # define the fields for items
    product_cat = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    product_id = scrapy.Field()
    product_url = scrapy.Field()
    data_id = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    item_info = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
