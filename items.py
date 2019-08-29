# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.org/en/latest/topics/items.html

from scrapy import Item,Field


class StartItem(Item):
    retailer_sku = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    name = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
