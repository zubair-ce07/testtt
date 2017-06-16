import scrapy


class KmartItem(scrapy.Item):
    name = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
