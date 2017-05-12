import scrapy


class Product(scrapy.Item):

    """object to save scraped data"""
    retailer_sku = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()