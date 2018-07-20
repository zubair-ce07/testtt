import scrapy
import re

from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class CraigslistItem(scrapy.Item):
    Title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst())
    URL = scrapy.Field(
        output_processor=TakeFirst(),)
    Location = scrapy.Field(
        input_processor=MapCompose(remove_tags, lambda x: x[2:-1]),
        output_processor=TakeFirst())
    datetime = scrapy.Field(
        output_processor=TakeFirst()
    )
