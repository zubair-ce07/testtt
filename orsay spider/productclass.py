import scrapy

class Product(scrapy.Item):

    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field() 
    discription = scrapy.Field()
    image_urls = scrapy.Field()
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    color_requests = scrapy.Field()