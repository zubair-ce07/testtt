# -*- coding: utf-8 -*-
from scrapy import Item, Field


class ProductItem(Item):
    # define the fields for your item here like:
    name = Field()
    url = Field()
    image_urls = Field()
    label = Field()
    price = Field()
    colors = Field()
    detail = Field()
    features = Field()
    materials = Field()
