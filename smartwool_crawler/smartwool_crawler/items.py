# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst , MapCompose


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    skus_out = list
    category_out = list
    image_urls_out = list
    description_in = MapCompose(str.strip)
    care_out = list
    size_out = list
    prices_detail = list

class SmartwoolCrawlerItem(scrapy.Item):
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
    size_key = scrapy.Field()
    size = scrapy.Field()
    color_key = scrapy.Field()
    prices_detail = scrapy.Field()
