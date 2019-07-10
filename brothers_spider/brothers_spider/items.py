# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ProductItem(Item):
    name = Field()
    category = Field()
    description = Field()
    gender = Field()
    image_urls = Field()
    price = Field()
    previous_price = Field()
    skus = Field()
    product_id = Field()
    request = Field()
