# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CecilItem(Item):
    # define the fields for your item here like:
    name = Field()
    available = Field()
    category = Field()
    subcategory = Field()
    images = Field()
    pid = Field()
    description = Field()
    attributes = Field()
    skus = Field()
    url = Field()
