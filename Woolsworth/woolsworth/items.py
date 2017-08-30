import scrapy


class Product(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    retailer_id = scrapy.Field()
    details = scrapy.Field()
