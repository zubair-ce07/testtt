import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def format_value(value):
    return "None" if value is None else value.strip()


class ProductItem(scrapy.Item):
    gender = scrapy.Field(
        output_processor=Compose(TakeFirst(), format_value),
    )
    retailer_sku = scrapy.Field(
        output_processor=TakeFirst(),
    )
    image_urls = scrapy.Field()
    description = scrapy.Field(
        output_processor=MapCompose(format_value)
    )
    category = scrapy.Field()
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    brand = scrapy.Field(
        output_processor=Compose(TakeFirst(), format_value)
    )
    skus = scrapy.Field()
