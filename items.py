# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SweatybettyItem(scrapy.Item):
    brand = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    gender = scrapy.Field()
    product_name = scrapy.Field()
    skus = scrapy.Field()
    category = scrapy.Field()
    image_url = scrapy.Field()
    video_url = scrapy.Field()
    product_id = scrapy.Field()

