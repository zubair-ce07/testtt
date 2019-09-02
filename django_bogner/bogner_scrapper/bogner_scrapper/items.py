from scrapy import Item, Field


class BognerItem(Item):
    url = Field()
    retailer_sku = Field()
    category = Field()
    gender = Field()
    brand = Field()
    name = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    market = Field()
    retailer = Field()
    skus = Field()
    price = Field()
    currency = Field()
