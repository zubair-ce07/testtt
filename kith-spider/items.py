import scrapy

class KithItem(scrapy.Item):
    skus = scrapy.Field()
    image_link = scrapy.Field()

