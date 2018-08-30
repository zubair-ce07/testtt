import scrapy


class Item(scrapy.Item):
    retailer_sku = scrapy.Field()
    brand = scrapy.Field()
    categories = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    gender = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    meta = scrapy.Field()
