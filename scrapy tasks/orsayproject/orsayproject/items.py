"""
This module hold page data.
"""
import scrapy


class OrsayprojectItem(scrapy.Item):
    """This class hold items"""
    url = scrapy.Field()
    desc_url = scrapy.Field()
    item_description_url = scrapy.Field()
    item_title = scrapy.Field()
    item_price = scrapy.Field()
    item_sizes = scrapy.Field()
    item_details = scrapy.Field()
    item_description = scrapy.Field()
