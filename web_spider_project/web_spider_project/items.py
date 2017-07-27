# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class HypedcItem(Item):
    item_id = Field()
    url = Field()
    name = Field()
    brand = Field()
    description = Field()
    currency = Field()
    is_discounted = Field()
    price = Field()
    old_price = Field()
    color_name = Field()
    image_urls = Field()


class WebSpiderProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

