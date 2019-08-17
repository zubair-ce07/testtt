from scrapy import Field, Item


class OnlyItem(Item):
    name = Field()
    description = Field()
    retailer_sku = Field()
    image_urls = Field()
    care = Field()
    url = Field()
    lang = Field()
    brand = Field()
    category = Field()
    crawl_start_time = Field()
    date = Field()
    crawl_id = Field()
    market = Field()
    retailer = Field()
    gender = Field()
    price = Field()
    skus = Field()
    meta = Field()
