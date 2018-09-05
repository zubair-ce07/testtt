from scrapy import Item, Field


class Garment(Item):
    retailer_sku = Field()
    name = Field()
    image_urls = Field()
    lang = Field()
    gender = Field()
    category = Field()
    industry = Field(default=None)
    brand = Field()
    url = Field()
    market = Field()
    trail = Field()
    retailer = Field()
    url_original = Field()
    description = Field()
    care = Field()
    skus = Field()
