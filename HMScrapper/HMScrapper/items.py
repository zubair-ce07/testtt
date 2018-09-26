# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field


class HmscrapperItem(Item):
    name = Field()
    price = Field()
    concept = Field()
    care_info = Field()
    item_code = Field()
    description = Field()
    composition = Field()
