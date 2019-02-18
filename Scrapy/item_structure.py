from scrapy import Item as ScrapyItem, Field


class Item(ScrapyItem):
    name = Field()
    retailer_sku = Field()
    url = Field()
    spider_name = Field()
    market = Field()
    retailer = Field()
    brand = Field()
    care = Field()
    category = Field()
    description = Field()
    image_urls = Field()
    trail = Field()
    skus = Field()
    meta = Field()
    gender = Field()
