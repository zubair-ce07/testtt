# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    skus_out = list
    category_out = list
    image_urls_out = list
    name_out = list
    requests_out = list


class SoftSurroundingsCrawlerItem(scrapy.Item):
    pid = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    requests = scrapy.Field()

