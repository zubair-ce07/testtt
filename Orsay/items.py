# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OrsayItem(scrapy.Item):
    """Item class which contains all the required
    fields which has to be crawled from the website
    """

    _id = scrapy.Field()    # Defined id for checking repetition
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    pass
