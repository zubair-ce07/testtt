# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class ProductItem(Item):
    brand = Field()
    retailer_sku = Field()
    name = Field()
    description = Field()
    care = Field()
    category = Field()
    url = Field()
    original_url = Field()
    image_urls = Field()
    skus = Field()


class SkuItem(Item):
    size = Field()
    price = Field()
    color = Field()
    currency = Field()
    stock = Field()
