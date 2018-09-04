"""
This module hold page data.
"""
import scrapy


class OnsayprojectItem(scrapy.Item):
    """This method hold field data"""
    url = scrapy.Field()
    desc_url = scrapy.Field()
    item_description_url = scrapy.Field()
    item_title = scrapy.Field()
    item_price = scrapy.Field()
    item_sizes = scrapy.Field()
    item_details = scrapy.Field()
    item_description = scrapy.Field()
