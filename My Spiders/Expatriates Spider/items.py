from scrapy import Item, Field

class Classified(Item):
    name = Field()
    date = Field()
    category = Field()
    region = Field()
    classified_id = Field()
    phone = Field()
    description = Field()
    image_urls = Field()
    url = Field()
