import scrapy
from scrapy.item import Field, Item


class GoSportItem(Item):
    retailer_sku = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    name = Field()
    description = Field()
    image_urls = Field()
    skus = Field()   
