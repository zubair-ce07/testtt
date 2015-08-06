# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class gulItem(scrapy.Item):
    item_code= scrapy.Field()
    item_price= scrapy.Field()
    item_url= scrapy.Field()
    item_image_url= scrapy.Field()
    item_brand_id = scrapy.Field()
    item_category_name= scrapy.Field()
    item_description= scrapy.Field()
    item_is_avaiable= scrapy.Field()

