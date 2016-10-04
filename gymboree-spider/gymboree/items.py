
import scrapy


class GarmentItem(scrapy.Item):
    brand = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    currency = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    spider_name = scrapy.Field()
    trail = scrapy.Field()
    url = scrapy.Field()