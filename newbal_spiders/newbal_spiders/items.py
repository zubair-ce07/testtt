# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy import Item


class NewbalanceItem(Item):
    product_url = Field()
    product_id = Field()
    title = Field()
    category = Field()
    description = Field()
    locale = Field()
    currency = Field()
    variationitems = Field()
    # sizeitem = Field()
