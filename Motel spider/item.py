import scrapy


class Product(scrapy.Item):

    """object to save scraped data"""
    sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    gender = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    details = scrapy.Field()


