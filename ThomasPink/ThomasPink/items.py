"""
This module holds crawled data items.
"""
import scrapy


class ThomaspinkItem(scrapy.Item):
    """This class holds item data fields."""
    item_detail_url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    item_id = scrapy.Field()
    description = scrapy.Field()
    delivery_details = scrapy.Field()
    