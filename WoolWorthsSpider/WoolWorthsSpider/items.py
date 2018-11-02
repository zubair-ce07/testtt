# -*- coding: utf-8 -*-
from scrapy import Item, Field


class WoolworthsItem(Item):
    name = Field()
    brand = Field()
    price = Field()
    cup_price = Field()
    old_price = Field()
    saving = Field()
    is_new = Field()
    is_special = Field()
    detail = Field()
    ingredients = Field()
    nutrition = Field()
    allergens = Field()
