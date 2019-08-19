import scrapy


class Item(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    previous_prices = scrapy.Field()
    currency = scrapy.Field()
    meta = scrapy.Field()
