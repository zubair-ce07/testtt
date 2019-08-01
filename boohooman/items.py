""""Boohooman Items Module.

This is a module for Boohooman product Items
"""
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    """Product Item.

    This is a class for boohooman item
    """

    product_code = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_description = scrapy.Field()
    product_category = scrapy.Field()
    product_link = scrapy.Field()
    data_skus = scrapy.Field()


class ProductSkus(scrapy.Item):
    """Product Skus Item.

    This is a product item data skus
    """

    color = scrapy.Field()
    sizes = scrapy.Field()
    pictures = scrapy.Field()
