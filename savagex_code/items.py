import scrapy


class SavagexItem(scrapy.Item):
    brand = scrapy.Field()
    trail = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    requests = scrapy.Field()
    pass

