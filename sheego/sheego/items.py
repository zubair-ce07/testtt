# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class SheegoItem(Item):
    # define the fields for your item here like:
    url_original = Field()
    pid = Field()
    name = Field()
    brand = Field()
    image_urls = Field()
    description = Field()
    category = Field()
    skus = Field()
    care = Field()
    gender = Field()
