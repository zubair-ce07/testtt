import scrapy


class ProductItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
