# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity


def clean_values(self, values):
    # full_form = ""
    all_values = [value.strip("\t\r\n\xa0") for value in values if value.strip("\t\r\n\xa0")]
    return " ".join(all_values)


class ProductItem(scrapy.Item):
    category = scrapy.Field()
    segment_1 = scrapy.Field()
    segment_2 = scrapy.Field()
    segment_3 = scrapy.Field()
    segment_4 = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    form = scrapy.Field()
    ean = scrapy.Field()


class ProdcutItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

    price_in = clean_values
    form_in = clean_values
    ean_out = Identity()


class CooconcenterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
