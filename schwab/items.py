# -*- coding: utf-8 -*-
import scrapy


class SchwabItem(scrapy.Item):
    title = scrapy.Field()
    retailer_sku = scrapy.Field()
    care_and_description = scrapy.Field()
    features = scrapy.Field()
    image_urls = scrapy.Field()
    categories = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
