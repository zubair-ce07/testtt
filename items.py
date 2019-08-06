from scrapy import Item,Field


class BeyondlimitItem(Item):
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
    care = Field()
    image_urls = Field()
    skus = Field()
    trail = Field()
