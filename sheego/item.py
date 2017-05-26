import scrapy


class Product(scrapy.Item):

    """object to save scraped data"""
    sku = scrapy.Field()
    brand = scrapy.Field()
    detail_points = scrapy.Field()
    image_urls = scrapy.Field()
    gender = scrapy.Field()
    care = scrapy.Field()
    skus = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()