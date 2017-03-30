# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawler1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class KidvaiPost(scrapy.Item):
    url = scrapy.Field()
    name_id = scrapy.Field()
    title = scrapy.Field()
    body_text = scrapy.Field()
    labels = scrapy.Field()
    posted_by = scrapy.Field()
    posted_time = scrapy.Field()
    comments = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


class HypedcProduct(scrapy.Item):
    url = scrapy.Field()
    product_id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    market = scrapy.Field()
    merch_info = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()


class GenericProduct(scrapy.Item):
    url = scrapy.Field()
    product_id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    market = scrapy.Field()
    merch_info = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()


class JelmoliProduct(scrapy.Item):
    url = scrapy.Field()
    product_id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    market = scrapy.Field()
    merch_info = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()
    industry = scrapy.Field()
