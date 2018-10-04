import scrapy

class Product(scrapy.Item):

    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field() 
    discription = scrapy.Field()
    image_urls = scrapy.Field()
    retailer_skus = scrapy.Field()
    name = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    color_links = scrapy.Field()