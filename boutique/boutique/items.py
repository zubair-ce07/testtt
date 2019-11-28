# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BoutiqueItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    market = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    sku_list = scrapy.Field()
