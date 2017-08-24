# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProfileItem(scrapy.Item):
    employmentHistory = scrapy.Field()
    overview = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    skills = scrapy.Field()
    tests = scrapy.Field()
    assignments = scrapy.Field()
    portfolios = scrapy.Field()
    education = scrapy.Field()
    url = scrapy.Field()
    workHistory = scrapy.Field()
    title = scrapy.Field()
    identity = scrapy.Field()
