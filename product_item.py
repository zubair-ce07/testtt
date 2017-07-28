import scrapy
from scrapy import Field


class Product(scrapy.Item):
    brand = Field()
    care = Field()
    category = Field()
    description = Field()
    gender = Field()
    image_urls = Field()
    name = Field()
    retailer_sku = Field()
    skus = Field()
    url = Field()
    url_original = Field()


class ChildProduct(scrapy.Item):
    items = Field()


class GrandChildProduct(scrapy.Item):
    items = Field()


class Count(scrapy.Item):
    counter = Field()
