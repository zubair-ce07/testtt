import scrapy
import re

from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags


class CraigslistItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags),)
    URL = scrapy.Field()
    location = scrapy.Field(
        input_processor=MapCompose(remove_tags, lambda x: x[2:-1]),)
    datetime = scrapy.Field()
