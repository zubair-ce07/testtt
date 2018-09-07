# -*- coding: utf-8 -*-
from scrapy import Item, Field


class ProductItem(Item):
    # define the fields for your item here like:
    name = Field()
    url = Field()
    labels = Field()
    detail = Field()
    material = Field()
    image_urls = Field()
    colors = Field()
    skus = Field()
