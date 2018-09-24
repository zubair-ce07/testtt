# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class Product(scrapy.Item):
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
    value = [txt.strip() for txt in value]
    value = list(filter(lambda txt: txt != '', value))[0]
    value_splited = value.split(">")
    return value_splited[1]


def filter_type(self, value):
    value = [txt.strip() for txt in value]
    value = list(filter(lambda txt: txt != '', value))[0]
    value_splited = value.split(">")
    return value_splited[2]


def filter_code(self, value):
    value = value[0]
    return value[value.find("sp=")+3:]


def filter_price(self, value):
    value = value[0]
    return value[value.find("HK$")+3:]


def prepare_urls(self, value, loader_context):
    return [loader_context['response'].urljoin(url) for url in value]


class ProductLoader(ItemLoader):
    code_in = filter_code
    code_out = TakeFirst()
    brand_out = TakeFirst()
    categories_in = filter_category
    categories_out = TakeFirst()
    description_out = TakeFirst()
    name_out = TakeFirst()
    price_in = filter_price
    price_out = TakeFirst()
    product_type_in = filter_type
    product_type_out = TakeFirst()
    packaging_out = TakeFirst()
    currency_out = TakeFirst()
    image_urls_in = prepare_urls
