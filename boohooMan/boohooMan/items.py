# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoohoomanItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    item_detail = scrapy.Field()
    colors = scrapy.Field()
    url = scrapy.Field()
    retailer_sku = scrapy.Field()
    retailer = scrapy.Field()
    lang = scrapy.Field()
