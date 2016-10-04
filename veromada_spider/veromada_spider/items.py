# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VeromadaSpiderItem(scrapy.Item):

    spider_name = scrapy.Field()
    retailer = scrapy.Field()
    currency = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    product_id = scrapy.Field()
    description = scrapy.Field()
    selected_color = scrapy.Field()
    retailer_sku = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    url_original = scrapy.Field()
    image_urls = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()
    color_urls = scrapy.Field()