import scrapy


class KmartItem(scrapy.Item):
    name = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    gender = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field()
