# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WoolrichItem(scrapy.Item):
    product_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    img_urls = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    care = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    previous_price = scrapy.Field()
    pending_requests = scrapy.Field()
