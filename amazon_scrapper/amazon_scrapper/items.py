import scrapy
from scrapy.loader.processors import TakeFirst

from amazon_scrapper.processors import StripString, StripRating


class Product(scrapy.Item):
    ASIN = scrapy.Field(input_processor=StripString(), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=StripString(), output_processor=TakeFirst())
    name = scrapy.Field(input_processor=StripString(), output_processor=TakeFirst())
    source_url = scrapy.Field(output_processor=TakeFirst())
    department = scrapy.Field(output_processor=TakeFirst())
    image_url = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=StripRating(), output_processor=TakeFirst())
