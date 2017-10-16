import scrapy


class IntersportItem(scrapy.Item):
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    url = scrapy.Field()
    skus = scrapy.Field()
    lang = scrapy.Field()
    request_queue = scrapy.Field()
