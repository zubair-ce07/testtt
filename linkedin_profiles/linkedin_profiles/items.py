# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinProfilesItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    job_title = scrapy.Field()
    location = scrapy.Field()
    industry = scrapy.Field()
    summary = scrapy.Field()
    extra_info = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    languages = scrapy.Field()
    skills = scrapy.Field()
    pass
