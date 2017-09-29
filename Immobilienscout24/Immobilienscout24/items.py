# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Immobilienscout24Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    property_count_in_city = scrapy.Field()
    property_type = scrapy.Field()
    type_of_listing = scrapy.Field()
    property_subtype = scrapy.Field()
    city = scrapy.Field()
    crawl_datetime = scrapy.Field()
    agent = scrapy.Field()
    property_name = scrapy.Field()
    property_address = scrapy.Field()
    category = scrapy.Field()
