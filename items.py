import scrapy


class ProductInfo(scrapy.Item):
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    skus = scrapy.Field()
    gender = scrapy.Field()
    brand = scrapy.Field()
    date = scrapy.Field()
