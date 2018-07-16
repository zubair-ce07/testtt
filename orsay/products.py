from scrapy import Field
from scrapy import Item


class Product(Item):
    brand = Field()
    care = Field()
    category = Field()
    description = Field()
    image_urls = Field()
    name = Field()
    retailer_sku = Field()
    skus = Field()
    url = Field()
