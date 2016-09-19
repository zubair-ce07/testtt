# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JackwillsItem(scrapy.Item):
    spider_name = scrapy.Field()
    retailer = scrapy.Field()
    currency = scrapy.Field()
    market = scrapy.Field()
    category = scrapy.Field()
    product_hash = scrapy.Field()
    retailer_sku = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    outlet = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    industry = scrapy.Field()


