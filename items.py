import scrapy


class BeyondlimitItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    lang = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    market = scrapy.Field()
    retailer = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    trail = scrapy.Field()
