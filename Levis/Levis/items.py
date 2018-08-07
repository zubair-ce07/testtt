# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    lang = scrapy.Field()
    uuid = scrapy.Field()
    trail = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    industry = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    market = scrapy.Field()
    retailer = scrapy.Field()
    crawl_id = scrapy.Field()
    url_original = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    out_of_stock = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    spider_name = scrapy.Field()
    crawl_start_time = scrapy.Field()

