import re
import scrapy

from scrapy.loader.processors import Join, MapCompose, TakeFirst

def split_price(price):
    return float(re.match(r'(\W+)(\d*[,]*\d*[.]*\d*)', price).group(2).replace(',', ''))

def split_currency(price):
    return re.match(r'(\W+)(\d*[,]*\d*[.]*\d*)', price).group(1)

class Product(scrapy.Item):
    retailer_sku = scrapy.Field(
        output_processor = Join()
    )
    lang = scrapy.Field(
        output_processor = Join()
    )
    gender = scrapy.Field(
        output_processor = Join()
    )
    category = scrapy.Field()
    url = scrapy.Field(
        output_processor = Join()
    )
    date = scrapy.Field(
        output_processor = TakeFirst()
    )
    market = scrapy.Field(
        output_processor = TakeFirst()
    )
    name = scrapy.Field(
        output_processor = Join()
    )
    desc = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        input_processor = MapCompose(split_price),
        output_processor = TakeFirst()
    )
    currency = scrapy.Field(
        input_processor = MapCompose(split_currency),
        output_processor = TakeFirst()
    )

class Sku(scrapy.Item):
    price = scrapy.Field(
        input_processor = MapCompose(split_price),
        output_processor = TakeFirst()
    )
    currency = scrapy.Field(
        input_processor = MapCompose(split_currency),
        output_processor = TakeFirst()
    )
    previous_price = scrapy.Field(
        output_processor = TakeFirst()
    )
    color = scrapy.Field(
        output_processor = Join()
    )
    size = scrapy.Field(
        output_processor = Join()
    )
    availability = scrapy.Field(
        output_processor = TakeFirst()
    )
    