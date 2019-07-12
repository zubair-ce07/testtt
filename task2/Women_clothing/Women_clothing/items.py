# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class BeginningboutiqueItem(Item):
    retailer_sku = Field()
    gender = Field()
    trail = Field()
    category = Field()
    industry = None
    brand = Field()
    url = Field()
    market = Field()
    retailer = Field()
    url_original = Field()
    product_name = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
    price = Field()
    currency = Field()
    spider_name = Field()
    crawl_start_time = Field()
