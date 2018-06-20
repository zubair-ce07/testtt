import scrapy

from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


def dimension_format(value):
    unit = 'cm'
    value = value.strip()

    if unit in value:
        return value
    
    return value + unit


class Product(scrapy.Item):
    artist = Field()
    image = Field()
    path = Field()
    url = Field(
        output_processor=TakeFirst()
    )
    title = Field(
        output_processor=TakeFirst()
    )
    height = Field(
        input_processor=MapCompose(dimension_format),
        output_processor=TakeFirst()
    )
    width = Field(
        input_processor=MapCompose(dimension_format),
        output_processor=TakeFirst()
    )
    description = Field(
        output_processor=TakeFirst()
    )

    
