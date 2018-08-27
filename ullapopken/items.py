import scrapy


class Item(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    categories = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    gender = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    currency = scrapy.Field()
    image_urls = scrapy.Field()
    requests = scrapy.Field()
