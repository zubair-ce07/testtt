import scrapy


class BognerItem(scrapy.Item):
    url = scrapy.Field()
    retailer_sku = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    retailer = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
