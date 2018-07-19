import scrapy


class DecimasItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    categories = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
