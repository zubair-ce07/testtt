import scrapy


class Product(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    image_urls_requests = scrapy.Field()
