# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LandmarkcrawlerItem(scrapy.Item):
    lmid = scrapy.Field()
    search_query = scrapy.Field()
    review_count = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field()
    operating_hours = scrapy.Field()
    landmark = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    country = scrapy.Field()
    url = scrapy.Field()
