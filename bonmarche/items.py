from scrapy import Item, Field


class ProductItem(Item):
    retailer_sku = Field()
    trail = Field()
    gender = Field()
    category = Field()
    brand = Field()
    market = Field()
    retailer = Field()
    url = Field()
    name = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
    currency = Field()
    spider_name = Field()
    requests = Field()
