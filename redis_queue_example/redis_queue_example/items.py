# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
import re

def filter_currency(value):
    if value == '\u20ac': #ToDo use unicode lib
        return "EUR"
    else:
        return None

def filter_stock(value):
    if value:
        return True

def to_float(value):
    return float(value.split(" ")[0].replace(",", "."))

def to_int(value):
    return int(value)


def clean_data(input):
    if type(input) is str:
        return re.sub(r'[\n\t\s]+', ' ', input)
    elif type(input) is list:
        return [re.sub(r'[\n\t\s]+', ' ', i) for i in input]
    else:
        return input


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    description_in = MapCompose(clean_data, str.strip)
    currency_in = MapCompose(filter_currency)
    image_urls_out = list
    care_out = list
    price_in = MapCompose(clean_data, str.strip, to_float)
    out_of_stock_in = MapCompose(TakeFirst(), filter_stock)
    retailer_sk_in = MapCompose(to_int)


class OrsayItemLoaderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    skus = scrapy.Field()
    date = scrapy.Field()
    crawl_start_time = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    lang = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    retailer_sk = scrapy.Field()
    image_urls = scrapy.Field()
    care = scrapy.Field()
    currency = scrapy.Field()
    gender = scrapy.Field()
    colour = scrapy.Field()
    out_of_stock = scrapy.Field()
    size = scrapy.Field()
    size_input = scrapy.Field()


class OrsaySkuItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    currency = scrapy.Field()
    colour = scrapy.Field()
    out_of_stock = scrapy.Field()
    size = scrapy.Field()
