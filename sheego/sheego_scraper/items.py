# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SheegoScraperItem(scrapy.Item):
    all_colors = scrapy.Field()

    spider_name = scrapy.Field()
    currency = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    url_original = scrapy.Field()
    image_urls = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()
    requests = scrapy.Field()
    lang = scrapy.Field()
    date = scrapy.Field()
    oos_request = scrapy.Field()
