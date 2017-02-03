from scrapy.item import Item, Field


class OrsayItem(Item):
    spider_name = Field()
    url = Field()
    retailer = Field()
    brand = Field()
    currency = Field()
    market = Field()
    lang = Field()
    category = Field()
    name = Field()
    description = Field()
    product_hash = Field()
    price = Field()
    color = Field()
    image_urls = Field()
    care = Field()
    skus = Field()
