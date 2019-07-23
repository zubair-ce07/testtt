from scrapy import Field, Item


class BeyondLimitItem(Item):
    name = Field()
    gender = Field()
    description = Field()
    retailer_sku = Field()
    image_urls = Field()
    care = Field()
    url = Field()
    lang = Field()
    brand = Field()
    category = Field()
    skus = Field()
    crawl_start_time = Field()
    date = Field()
    crawl_id = Field()
    market = Field()
    retailer = Field()
