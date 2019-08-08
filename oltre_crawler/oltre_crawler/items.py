# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OltreCrawlerItem(scrapy.Item):
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    date = scrapy.Field()
    market = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field()
    requests = scrapy.Field()
    spider_name = scrapy.Field()
