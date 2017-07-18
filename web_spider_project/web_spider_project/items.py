# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class HypedcProductAttr(Item):
    Item_Id = Field()
    Url = Field()
    Name = Field()
    Brand = Field()
    Description = Field()
    Currency = Field()
    Is_Discounted = Field()
    Price = Field()
    Old_Price = Field()
    Color_Name = Field()
    Image_Urls = Field()


class WebSpiderProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
