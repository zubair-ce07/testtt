# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlueflyItem(scrapy.Item):
    product_id = scrapy.Field()
    merch_info = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    product_title = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()


class SkuItem(scrapy.Item):
    def __setitem__(self, key, value):
        self._values[key] = value


class ArbitraryItem(scrapy.Item):
    colour = scrapy.Field()
    price = scrapy.Field()
    previous_prices = scrapy.Field()
    size = scrapy.Field()
