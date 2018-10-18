# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity


def clean_values(self, values):
    all_values = [value.strip("\t\r\n\xa0") for value in values if value.strip("\t\r\n\xa0")]
    return " ".join(all_values)


def ean_clean(self, ean):
    return ean[0].replace("EAN : ", "")


def image_url_process(self, urls):
    urls = ["https:{}".format(url) for url in urls]
    return [url.replace("180x240", "750x1000") for url in urls]


class ProductItem(scrapy.Item):
    category = scrapy.Field()
    segment_1 = scrapy.Field()
    segment_2 = scrapy.Field()
    segment_3 = scrapy.Field()
    segment_4 = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    form = scrapy.Field()
    ean = scrapy.Field()
    variant = scrapy.Field()
    image_urls = scrapy.Field()


class ProdcutItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

    price_in = clean_values
    form_in = clean_values
    ean_in = ean_clean
    image_urls_in = image_url_process
    image_urls_out = Identity()
