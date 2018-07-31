from scrapy.item import Item, Field


class HugoBossItem(Item):
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
