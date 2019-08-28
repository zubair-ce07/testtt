# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    currency = scrapy.Field()
    market = scrapy.Field()
    retailer = scrapy.Field()
    url_original = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    spider_name = scrapy.Field()
    crawl_start_time = scrapy.Field()
