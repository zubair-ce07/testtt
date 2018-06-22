import scrapy

from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from w3lib.html import remove_tags


def format_price(value):
    return float(value)


def format_description(value):
    return remove_tags(value)


class Product(Item):
    url = Field(
        output_processor=TakeFirst()
    )
    code = Field(
        output_processor=TakeFirst()
    )
    brand = Field(
        output_processor=TakeFirst()
    )
    name = Field(
        output_processor=TakeFirst()
    )
    price = Field(
        output_processor=TakeFirst()
    )
    currency = Field(
        output_processor=TakeFirst()
    )
    previous_price = Field(
        output_processor=TakeFirst()
    )
    description = Field(
        input_processor=MapCompose(format_description),
        output_processor=TakeFirst()
    )
    categories = Field(
        output_processor=TakeFirst()
    )
    availability = Field(
        output_processor=TakeFirst()
    )
    packaging = Field(
        output_processor=TakeFirst()
    )
    colour = Field()
    image_urls = Field()
    reviews_count = Field(
        output_processor=TakeFirst()
    )
    reviews_score = Field(
        output_processor=TakeFirst()
    )
    barcode = Field(
        output_processor=TakeFirst()
    )
    store_name = Field(
        output_processor=TakeFirst()
    )
    website_name = Field(
        output_processor=TakeFirst()
    )
    product_type = Field(
        output_processor=TakeFirst()
    )
    price_per_unit = Field(
        output_processor=TakeFirst()
    )
    
