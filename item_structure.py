from scrapy import Item as scrapy_item, Field


class Item(scrapy_item):
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
