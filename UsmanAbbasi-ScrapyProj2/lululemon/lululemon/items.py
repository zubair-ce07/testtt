# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LululemonItem(scrapy.Item):
    url = scrapy.Field()
    item_id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    currency = scrapy.Field()
    image_urls = scrapy.Field()
    sku = scrapy.Field()
