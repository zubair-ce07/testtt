from scrapy import Field, Item


class KleineskarussellItem(Item):
    retailer_sku = Field()
    name = Field()
    gender = Field()
    category = Field()
    description = Field()
    url = Field()
    brand = Field()
    care = Field()
    image_urls = Field()
    skus = Field()

