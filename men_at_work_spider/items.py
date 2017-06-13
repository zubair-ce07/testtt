import scrapy

class MenAtWorkItem(scrapy.Item):
    brand = scrapy.Field()
    name = scrapy.Field()
    image_urls = scrapy.Field()
    url = scrapy.Field()
    skus = scrapy.Field()
    description = scrapy.Field()