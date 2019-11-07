import scrapy


class SnkrSpiderItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
