# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductSpiderItem(scrapy.Item):
    spider_name = scrapy.Field()
    retailer = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    market = scrapy.Field()
    color = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    img_urls = scrapy.Field()
    skus = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    gender = scrapy.Field()
    available_colors = scrapy.Field()





