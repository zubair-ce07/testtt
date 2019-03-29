# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def filter_description(value):
    if value is not "":
        return value


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    description_in = MapCompose(str.strip, filter_description)
    description_out = list
    care_in = MapCompose(str.strip)
    skus_out = list
    category_out = list


class BoutiqueCrawlerItem(scrapy.Item):
    pid = scrapy.Field()
    gender = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    category = scrapy.Field()

