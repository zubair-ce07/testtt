# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KithItem(scrapy.Item):
    product_id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    material = scrapy.Field()
    img_urls = scrapy.Field()
    currency = scrapy.Field()
    sizes = scrapy.Field()
    url = scrapy.Field()
