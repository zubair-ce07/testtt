from scrapy.item import Item, Field

import scrapy


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
