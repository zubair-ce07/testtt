# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ProductItem(Item):
    retailer_sku = Field()
    lang = Field()
    trail = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    date = Field()
    market = Field()
    url_original = Field()
    name = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
    out_of_stock = Field()
    price = Field()
    currency = Field()
