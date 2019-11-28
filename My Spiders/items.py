from scrapy import Item, Field


class Product(Item):
    retailer_sku = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    name = Field()
    description = Field()
    care = Field()
    skus = Field()
    requests = Field()
    image_urls = Field()
    out_of_stock = Field()
    image_urls = Field()
    trail = Field()
    requests = Field()
    meta = Field()
