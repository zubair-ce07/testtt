# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Product(Item):
    retailer_sku = Field()
    trail = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    market = Field()
    retailer = Field()
    name = Field()
    description = Field()
    images_url = Field()
    skus = Field()
    price = Field()
    currency = Field()
    meta = Field()


class Sku(Item):
    colour = Field()
    previous_prices = Field()
    size = Field()
    sku_id = Field()
