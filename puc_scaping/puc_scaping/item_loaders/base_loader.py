"""Base Loader"""
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class BaseLoader(ItemLoader):
    """Base Loader class for puc"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(remove_tags)
