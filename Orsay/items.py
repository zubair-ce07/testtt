# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join, MapCompose


class ScrapOrsayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class OrsayItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    brand = scrapy.Field(output_processor=TakeFirst())
    care = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field()
    image_urls = scrapy.Field()
    retailer_sku = scrapy.Field(output_processor=TakeFirst())
    skus = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())

