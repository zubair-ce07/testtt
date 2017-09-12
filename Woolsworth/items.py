import scrapy


class Product(scrapy.Item):
    url = scrapy.Field()
    retailer_id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    details = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
