from scrapy.item import Item, Field


class RunnersPointItem(Item):
    url = Field()
    spider_name = Field()
    retailer = Field()
    brand = Field()
    market = Field()
    lang = Field()
    currency = Field()
    category = Field()
    name = Field()
    description = Field()
    gender = Field()
    price = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
