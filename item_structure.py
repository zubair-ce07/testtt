from scrapy import Item as it, Field


class Item(it):
    name = Field()
    retailer_sku = Field()
    url = Field()
    spider_name = Field()
    market = Field()
    retailer = Field()
    brand = Field()
    care = Field()
    category = Field()
    description = Field()
    image_urls = Field()
    trail = Field()
    skus = Field()
