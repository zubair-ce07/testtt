# -*- coding: utf-8 -*-
import scrapy


class OrsayProduct(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    category = scrapy.Field()
    material = scrapy.Field()
    care = scrapy.Field()
    img_urls = scrapy.Field()
    skus = scrapy.Field()

    lang = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    crawl_start_time = scrapy.Field()


