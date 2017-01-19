# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WoolworthsItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    retailer = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    previous_price = scrapy.Field()
    image_urls = scrapy.Field()
    uuid = scrapy.Field()
    trail = scrapy.Field()
    date = scrapy.Field()
    spider_name = scrapy.Field()
    gender = scrapy.Field()
    currency = scrapy.Field()
    product_hash = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    industry = scrapy.Field()
    market = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    crawl_id = scrapy.Field()
    url_original = scrapy.Field()
    category = scrapy.Field()
    crawl_start_time = scrapy.Field()
    lang = scrapy.Field()
