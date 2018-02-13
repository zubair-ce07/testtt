# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class AldoshoesItem(scrapy.Item):
    category_names = scrapy.Field()
    brand = scrapy.Field()
    currency = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    language_code = scrapy.Field()
    base_sku = scrapy.Field()
    identifier = scrapy.Field()
    image_urls = scrapy.Field()
    description_text = scrapy.Field()
    referer_url = scrapy.Field()
    color_name = scrapy.Field()
    color_code = scrapy.Field()
    old_price_text = scrapy.Field()
    new_price_text = scrapy.Field()
    size_infos = scrapy.Field()
    available = scrapy.Field()

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


