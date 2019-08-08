from scrapy import Item, Field


class Product(Item):
    retailer_sku = Field()
    lang = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    market = Field()
    retailer = Field()
    name = Field()
    description = Field()
    image_urls = Field()
    skus = Field()
    property = Field()

