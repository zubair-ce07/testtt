# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JeniespiderItem(scrapy.Item):
    product_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    date = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    category = scrapy.Field()
    skus = scrapy.Field(type='list')
    market = scrapy.Field()
    brand = scrapy.Field()
    retailer = scrapy.Field()
