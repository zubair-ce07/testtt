# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class CaPucItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = Field()
    filed_on = Field()
    assignees = Field()
    industries = Field()
    filed_by = Field()
    proceeding_type = Field()
    title = Field()
    status = Field()
    state_id = Field()
    filings = Field()
