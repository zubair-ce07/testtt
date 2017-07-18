# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import TakeFirst


class AldowebcrawlerItem(scrapy.Item):
    pass


class AldoProductItem(scrapy.Item):
    variations = scrapy.Field(type='list')
    title = scrapy.Field(output_processor=TakeFirst())
    brand = scrapy.Field(output_processor=TakeFirst())
    locale = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    product_url = scrapy.Field(output_processor=TakeFirst())
    store_keeping_unit = scrapy.Field(output_processor=TakeFirst())


class AldoVariantionItem(scrapy.Item):
    sizes = scrapy.Field(type='list')
    image_urls = scrapy.Field(type='list')
    display_color_name = scrapy.Field(output_processor=TakeFirst())


class AldoSizeItem(scrapy.Item):
    price = scrapy.Field(output_processor=TakeFirst())
    size_name = scrapy.Field(output_processor=TakeFirst())
    is_available = scrapy.Field(output_processor=TakeFirst())
    is_discounted = scrapy.Field(output_processor=TakeFirst())
    discounted_price = scrapy.Field(output_processor=TakeFirst())
