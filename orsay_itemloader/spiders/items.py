# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class OrsayProduct(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    category = scrapy.Field()
    material = scrapy.Field()
    care = scrapy.Field()
    img_urls = scrapy.Field()
    skus = scrapy.Field()

    lang = scrapy.Field()


def clean_text(raw_text):
    if type(raw_text) is str:
        return re.sub(r'[\n\t\s]+', ' ', raw_text)
    elif type(raw_text) is list:
        return [re.sub(r'[\n\t\s]+', ' ', i) for i in raw_text]


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    price_in = MapCompose(clean_text, str.strip)
    name_in = MapCompose(clean_text, str.title)
    description_in = MapCompose(clean_text, str.strip)
    material_in = MapCompose(clean_text, str.strip)
    care_out = list
    img_urls_out = list


