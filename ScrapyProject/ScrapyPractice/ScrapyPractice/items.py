# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapypracticeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Record(scrapy.Item):
    docket = scrapy.Field()
    filler = scrapy.Field()
    description = scrapy.Field()
    date_filed = scrapy.Field()
