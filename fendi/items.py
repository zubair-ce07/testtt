from scrapy.item import Item, Field


class FendiItem(Item):
    original_url = Field()
    spider_name = Field()
    retailer = Field()
    category = Field()
    product_hash = Field()
    brand = Field()
    name = Field()
    description = Field()
    price = Field()
    image_urls = Field()
    currency = Field()
    market = Field()
    skus = Field()
