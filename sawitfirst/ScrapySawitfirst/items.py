from scrapy import Field
from scrapy import Item

class Item(Item):
    retailer_sku = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    name = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
    price = Field()
    previous_prices = Field()
    currency = Field()
    meta = Field()
