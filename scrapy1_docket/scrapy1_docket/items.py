# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DocketItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    docket = scrapy.Field()
    filer = scrapy.Field()
    description = scrapy.Field()
    filed_date = scrapy.Field()
    file_url = scrapy.Field()
