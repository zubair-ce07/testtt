# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawler2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # field1 = scrapy.Field()
    # field2 = scrapy.Field()

    spider_name = scrapy.Field()
    retailer = scrapy.Field()
    currency = scrapy.Field()
    market = scrapy.Field()
    category = scrapy.Field()
    uuid = scrapy.Field()
    retailer_sku = scrapy.Field()
    product_hash = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    trail = scrapy.Field()
    crawl_id = scrapy.Field()
    date = scrapy.Field()
    skus = scrapy.Field()
        # {
        # currency = scrapy.Field()
        # price = scrapy.Field()
        # out_of_stock = scrapy.Field()
        # colour = scrapy.Field()
        # size = scrapy.Field()
        # }
    care = scrapy.Field()
    lang = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    gender = scrapy.Field()
    industry = scrapy.Field()
    crawl_start_time = scrapy.Field()

    # pass

