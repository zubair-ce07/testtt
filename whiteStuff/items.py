import scrapy


class WhiteStuffItem(scrapy.Item):
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
