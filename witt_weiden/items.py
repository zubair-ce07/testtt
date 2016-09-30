# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WittWeidenSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()
    crawl_start_time = scrapy.Field()
    price = scrapy.Field()
    lang = scrapy.Field()
    spider_name = scrapy.Field()
    crawl_id = scrapy.Field()
    care = scrapy.Field()
    retailer_sku = scrapy.Field()
    retailer = scrapy.Field()
    gender = scrapy.Field()
    market = scrapy.Field()
    brand = scrapy.Field()
    date = scrapy.Field()
    uuid = scrapy.Field()
    skus = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    currency = scrapy.Field()
    url = scrapy.Field()
    product_hash = scrapy.Field()
    pass
