# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SweatBettyItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    name = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()
    retailer_sku = scrapy.Field()
    image_urls = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    currency = scrapy.Field()
    pass
