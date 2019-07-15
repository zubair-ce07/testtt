from scrapy.item import Item, Field


class NewyorkerItem(Item):
    sales_unit = Field()
    retailer_sku = Field()
    gender = Field()
    trail = Field()
    category = Field()
    industry = Field()
    brand = Field()
    url = Field()
    market = Field()
    url_original = Field()
    description = Field()
    image_urls = Field()
    skus = Field()
    price = Field()
    currency = Field()
    spider_name = Field()
    crawl_start_time = Field()
