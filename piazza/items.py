import scrapy


class ProductItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    trail = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    market = scrapy.Field()
    retailer = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    spider_name = scrapy.Field()
    pass


class SkuItem(scrapy.Item):
    price = scrapy.Field()
    currency = scrapy.Field()
    previous_price = scrapy.Field()
    size = scrapy.Field()
    color = scrapy.Field()
    pass