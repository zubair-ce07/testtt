import scrapy


class SheegoProduct(scrapy.Item):
    category = scrapy.Field()
    retailer_sku = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    date = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
    lang = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    gender = scrapy.Field()
    requests = scrapy.Field()
    oos_request = scrapy.Field()
