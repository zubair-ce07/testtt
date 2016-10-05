# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinProfileUrlItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    name = scrapy.Field()

class LinkedinProfilesItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
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
    profile_picture = scrapy.Field()
    certifications = scrapy.Field()
    volunteering = scrapy.Field()
    publications = scrapy.Field()
