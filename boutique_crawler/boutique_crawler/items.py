# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoutiqueCrawlerItem(scrapy.Item):
    pid = scrapy.Field()
    gender = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    category = scrapy.Field()

