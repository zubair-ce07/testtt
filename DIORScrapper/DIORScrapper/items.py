from scrapy import Item, Field


class DiorItem(Item):
    id = Field()
    url = Field()
    name = Field()
    sizes = Field()
    price = Field()
    brand = Field()
    colors = Field()
    status = Field()
    variant = Field()
    category = Field()
    image_urls = Field()
    description = Field()
    characteristics = Field()
