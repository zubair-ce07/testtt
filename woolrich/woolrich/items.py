# -*- coding: utf-8 -*-
import scrapy


class WoolRichItem(scrapy.Item):
    title = scrapy.Field()
    url_original = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    brand_name = scrapy.Field()
    requests = scrapy.Field()
    category = scrapy.Field()
    currency = scrapy.Field()
    care = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()
