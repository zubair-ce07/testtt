# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SheegoScraperItem(scrapy.Item):
    all_colors = scrapy.Field()

    spider_name = scrapy.Field()
    retailer = scrapy.Field()
    retailer_ID = scrapy.Field()
    currency = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    selected_color = scrapy.Field()
    retailer_sku = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    url_original = scrapy.Field()
    image_urls = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()
    xresponse = scrapy.Field()
    care = scrapy.Field()
    requests = scrapy.Field()
    lang = scrapy.Field()
    date = scrapy.Field()
    oos_request = scrapy.Field()