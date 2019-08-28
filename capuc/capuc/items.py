# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Docket(scrapy.Item):
    # define the fields for your item here like:
    major_parties = scrapy.Field()
    assignees = scrapy.Field()
    filed_on = scrapy.Field()
    industries = scrapy.Field()
    proceeding_type = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    slug = scrapy.Field()
    state = scrapy.Field()
    state_id = scrapy.Field()
    filings = scrapy.Field()
