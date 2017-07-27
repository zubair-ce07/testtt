# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HypedcItem(scrapy.Item):
    brand = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    other_colors = scrapy.Field()
    breadcrumb = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()
    skus = scrapy.Field()
