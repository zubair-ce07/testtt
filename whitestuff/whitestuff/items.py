import scrapy


class WhitestuffProduct(scrapy.Item):
    spider_name = scrapy.Field()
    retailer = scrapy.Field()
    currency = scrapy.Field()
    market = scrapy.Field()
    category = scrapy.Field()
    retailer_sku = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    industry = scrapy.Field()
    requests = scrapy.Field()
    url = scrapy.Field()
