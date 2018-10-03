"""
This module holds crawled data items.
"""
import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class Product(scrapy.Item):
    """This class holds item data fields."""
    item_detail_url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    product_id = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    title_description = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    more_description = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    full_price = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    sale_price = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    discount_upto = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
