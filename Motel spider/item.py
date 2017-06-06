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
    description = scrapy.Field()
    price = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    availability = scrapy.Field()


