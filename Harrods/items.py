# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class HarrodsItem(scrapy.Item):
    url = scrapy.Field()
    code = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    previous_price = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    availability = scrapy.Field()
    packaging = scrapy.Field()
    image_urls = scrapy.Field()
    reviews_count = scrapy.Field()
    reviews_score = scrapy.Field()
    barcode = scrapy.Field()
    store_name = scrapy.Field()
    website_name = scrapy.Field()
    product_type = scrapy.Field()
    price_per_unit = scrapy.Field()
    promotion = scrapy.Field()
    name_hk = scrapy.Field()
    brand_hk = scrapy.Field()


def filter_category(self, value):
    return value[2]


def filter_product_type(self, value):
    return value[1]


class ProductLoader(ItemLoader):
    brand_out = TakeFirst()
    categories_in = filter_category
    categories_out = TakeFirst()
    currency_out = TakeFirst()
    description_in = MapCompose(str.strip)
    description_out = Join()
    name_out = TakeFirst()
    price_out = TakeFirst()
    price_per_unit_out = TakeFirst()
    product_type_in = filter_product_type
    product_type_out = TakeFirst()
