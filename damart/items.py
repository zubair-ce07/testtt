# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DamartCrawlingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    ref_code = scrapy.Field()
    description = scrapy.Field()
    benefits = scrapy.Field()
    image_urls = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    composition =  scrapy.Field()
    colors = scrapy.Field()
    url = scrapy.Field()
    pass
