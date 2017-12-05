# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BerlinJobItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    perks = scrapy.Field()
    location = scrapy.Field()
    technologies = scrapy.Field()
    description = scrapy.Field()
