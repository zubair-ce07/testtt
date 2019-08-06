from scrapy import Item, Field


class ErnstingSpiderItem(Item):
    product_id = Field()
    name = Field()
    description = Field()
    category = Field()
    gender = Field()
    care = Field()
    url = Field()
    skus = Field()
    img_urls = Field()
    brand = Field()
    lang = Field()
    market = Field()
    date = Field()

