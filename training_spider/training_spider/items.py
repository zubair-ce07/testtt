from scrapy import Item, Field


class TrainingSpiderItem(Item):
    product_id = Field()
    product_name = Field()
    product_url = Field()
    country = Field()
    currency = Field()
    variations = Field()
