from scrapy import Field, Item


class SoftSurroundingsItem(Item):
    uuid = Field()
    care = Field()
    category = Field()
    description = Field()
    gender = Field()
    image_urls = Field()
    name = Field()
    price = Field()
    currency = Field()
    retailer_sku = Field()
    skus = Field()
    url_orignal = Field()
    market = Field()
    retailer = Field()
    date = Field()
    crawl_id = Field()
    spider_name = Field()
    crawl_start_time = Field()
    website_name = Field()
    meta = Field()
