# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class JackjonesItem(Item):
    # define the fields for your item here like:
    name = Field()
    category = Field()
    subcategory = Field()
    images = Field()
    pid = Field()
    article_number = Field()
    description = Field()
    attributes = Field()
    skus = Field()
    url= Field()
