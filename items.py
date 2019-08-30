# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class StartItem(Item):
    retailer_sku = Field()
    gender = Field()
    brand = Field()
    url = Field()
    care = Field()
    name = Field()
    description = Field()
    image_urls = Field()
    skus = Field()
    meta = Field()
    price = Field()
    out_of_stock = Field()
