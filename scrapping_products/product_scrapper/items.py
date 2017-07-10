# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductScrapperItem(scrapy.Item):
    product_id = scrapy.Field(type='str')
    name = scrapy.Field(type='str')
    product_desc = scrapy.Field(type='list')
    url = scrapy.Field(type='str')
    colors = scrapy.Field(type='list')
    image_urls = scrapy.Field(type='str')
    product_price = scrapy.Field(type='str')
    product_care = scrapy.Field(type='list')
    skus = scrapy.Field(type='list')
