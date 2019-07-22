import scrapy


class SnkrsItem(scrapy.Item):
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    trail = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    retailer = scrapy.Field()
    lang = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()


class SnkrsSkuItem(scrapy.Item):
    color = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    size = scrapy.Field()
    previous_prices = scrapy.Field()
    sku_id = scrapy.Field()
