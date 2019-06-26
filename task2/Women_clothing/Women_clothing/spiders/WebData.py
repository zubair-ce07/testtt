from scrapy.item import Item, Field


class WebData(Item):
    retailer_sku = Field()
    gender = Field(default="women")
    trail = Field()
    category = Field()
    industry = None
    brand = Field()
    url = Field()
    market = Field(default='AUS')
    retailer = Field()
    url_original = Field()
    product_name = Field()
    description = Field()
    care = Field()
    image_url = Field()
    skus = Field()
    price = Field()
    currence = Field()
    spider_name = Field(default='beginningboutique')
    crawl_start_time = Field()

