import scrapy


class SnkrsItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()  
    description = scrapy.Field() 
    care = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()
