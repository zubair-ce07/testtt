import scrapy

class OrsayItem(scrapy.Item):
    skus = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
