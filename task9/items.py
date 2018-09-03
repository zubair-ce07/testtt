import scrapy


class Product(scrapy.Item):
    gender = scrapy.Field()
    retailer_sku = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
