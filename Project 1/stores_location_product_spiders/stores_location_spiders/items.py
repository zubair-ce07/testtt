# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class StoresLocationItem(Item):
    city = Field()
    address = Field()
    country = Field()
    hours = Field()
    phone_number = Field()
    services = Field()
    state = Field()
    store_email = Field()
    store_floor_plan_url = Field()
    store_id = Field()
    store_image_url = Field()
    store_name = Field()
    store_url = Field()
    weekly_ad_url = Field()
    zipcode = Field()

	
class HhgreggItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    product_id = scrapy.Field()
    sku = scrapy.Field()
    model = scrapy.Field()
    rating = scrapy.Field()
    mpn = scrapy.Field()
    upc = scrapy.Field()
    trail = scrapy.Field()
    features = scrapy.Field()
    specifications = scrapy.Field()
    current_price = scrapy.Field()
    original_price = scrapy.Field()
    currency = scrapy.Field()
    source_url = scrapy.Field()
    primary_image_url = scrapy.Field()
    image_urls = scrapy.Field()
    items = scrapy.Field()
    available_online = scrapy.Field()
    available_instore = scrapy.Field()