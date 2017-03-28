# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Compose


class SheegoItem(scrapy.Item):
    brand = scrapy.Field(
        output_processor=Compose(lambda brands: brands[0], str.upper)
    )
    care = scrapy.Field(
        output_processor=TakeFirst()
    )
    category = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_urls = scrapy.Field()
    lang = scrapy.Field(
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    retailer_sku = scrapy.Field(
        output_processor=TakeFirst()
    )
    skus = scrapy.Field(
        output_processor=TakeFirst()
    )
    oos_request = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    url_original = scrapy.Field(
        output_processor=TakeFirst()
    )
