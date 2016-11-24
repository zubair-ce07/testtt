# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field


class DrykornItem(Item):
    skus = Field()
    date = Field()
    lang = Field()
    price = Field()
    name = Field()
    industry = Field()
    crawl_id = Field()
    image_urls = Field()
    product_hash = Field()
    gender = Field()
    retailer_sku = Field()
    market = Field()
    url_original = Field()
    trail = Field()
    category = Field()
    uuid = Field()
    description = Field()
    brand = Field()
    url = Field()
    spider_name = Field()
    currency = Field()
    crawl_start_time = Field()
    retailer = Field()
    care = Field()
