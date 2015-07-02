import scrapy

class WhitestuffUkItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    retailer_sku = scrapy.Field()
    url_original = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
    url = scrapy.Field()
    gender = scrapy.Field()
