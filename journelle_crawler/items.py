from scrapy import Item, Field


class ProductItem(Item):
    retailer_sku = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    date = Field()
    currency = Field()
    market = Field()
    retailer = Field()
    url_original = Field()
    name = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    price = Field()
    skus = Field()
    spider_name = Field()
    crawl_start_time = Field()
