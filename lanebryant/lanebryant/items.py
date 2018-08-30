from scrapy import Item, Field


class LanebryantItem(Item):
    retailer_sku = Field()
    trail = Field()
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
    currency = Field()
    requests = Field()
