# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    Id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    product_imgs = scrapy.Field()
    category = scrapy.Field()
    skus = scrapy.Field()
    urls = scrapy.Field()
    care = scrapy.Field()