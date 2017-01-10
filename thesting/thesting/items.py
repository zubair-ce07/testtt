# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TheStingItem(scrapy.Item):
    category = scrapy.Field()
    lang = scrapy.Field()
    trail = scrapy.Field()
    gender = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    industry = scrapy.Field()
    crawl_start_time = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    retailer_sku = scrapy.Field()
    currency = scrapy.Field()
    date = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()
    spider_name = scrapy.Field()
    market = scrapy.Field()
    crawl_id = scrapy.Field()
    retailer = scrapy.Field()
    price = scrapy.Field()
    previous_price = scrapy.Field()
    url_original = scrapy.Field()
    uuid = scrapy.Field()
