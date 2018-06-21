import scrapy

from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose


class Product(Item):
    url = Field()
    code = Field()
    brand = Field()
    name = Field()
    price = Field()
    currency = Field()
    previous_price = Field()
    description = Field()
    categories = Field()
    availability = Field()
    packaging = Field()
    image_urls = Field()
    reviews_count = Field()
    reviews_score = Field()
    barcode = Field()
    store_name = Field()
    website_name = Field()
    product_type = Field()
    price_per_unit = Field()


