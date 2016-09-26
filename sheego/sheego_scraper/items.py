# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SheegoScraperItem(scrapy.Item):
   
    date = scrapy.Field()
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    url_original = scrapy.Field()
    pid = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    skus = scrapy.Field()
    out_of_stock = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    lang = scrapy.Field()
    url = scrapy.Field()

