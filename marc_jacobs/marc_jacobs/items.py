from scrapy import Item, Field


class MarcJacobsItem(Item):
    url = Field()
    brand = Field()
    name = Field()
    image_urls = Field()
    description = Field()
    skus = Field()
