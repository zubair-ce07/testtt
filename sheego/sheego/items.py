"""
This module holds crawled data items.
"""
import scrapy


class SheegoItem(scrapy.Item):
    """This class holds item data fields."""
    item_detail_url = scrapy.Field()
    category = scrapy.Field()
    product_title = scrapy.Field()
    price = scrapy.Field()
    sizes = scrapy.Field()
    description = scrapy.Field()
