"""
This module holds crawled data items.
"""
import scrapy


class DemartItem(scrapy.Item):
    """This class holds item data fields."""
    item_detail_link = scrapy.Field()
    title = scrapy.Field()
    information = scrapy.Field()
    series = scrapy.Field()
    description = scrapy.Field()
 