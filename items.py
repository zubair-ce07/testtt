from scrapy.item import Item, Field


class AsicsItem(Item):
    spider_name = Field()
    retailer = Field()
    currency = Field()
    market = Field()
    category = Field()
    retailer_sku = Field()
    price = Field()
    description = Field()
    url_original = Field()
    brand = Field()
    color = Field()
    image_urls = Field()
    date = Field()
    skus = Field()
    care = Field()
    name = Field()
    url = Field()
    gender = Field()
    industry = Field()
    