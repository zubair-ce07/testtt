from scrapy import Field, Item


class BeyondLimitItem(Field):
    name = Field(),
    gender = Field(),
    description = Field(),
    retailer_sku = Field(),
    image_urls = Field(),
    care = Field(),
    url = Field(),
    lang = Field(),
    brand = Field(),
    category = Field(),
    color = Field(),
    skus = Field(),
    crawl_start_time = Field(),
    time = Field(),
    crawl_id = Field()
