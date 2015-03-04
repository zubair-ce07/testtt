# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ErnstingsItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    spider_name = scrapy.Field()
    description = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sk = scrapy.Field()
    image_urls = scrapy.Field()
    currency = scrapy.Field()
    care = scrapy.Field()
    color = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    brand = scrapy.Field()
    industry = scrapy.Field()
    gender = scrapy.Field()
