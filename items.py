"""
Models for scrapped Items of ernstings-family
Pylint Score: 10.00
"""

import scrapy                           # pylint: disable=import-error


class Product(scrapy.Item):             # pylint: disable=too-few-public-methods
    """product item"""
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()


class StoreKeepingUnits(scrapy.Item):   # pylint: disable=too-few-public-methods
    """SKU item"""
    price = scrapy.Field()
    currency = scrapy.Field()
    previous_prices = scrapy.Field()
    colour = scrapy.Field()
    size = scrapy.Field()
    out_of_stock = scrapy.Field()
    sku_id = scrapy.Field()
