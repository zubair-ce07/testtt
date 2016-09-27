from scrapy.item import Item, Field


class AsicsItem(Item):
    spider_name = Field()
    retailer = Field()
    currency = Field()
    price = Field()
    market = Field()
    color = Field()
    category = Field()
    description = Field()
    url_original = Field()
    brand = Field()
    img_urls = Field()
    sku = Field()
    name = Field()
    url = Field()
    gender = Field()
