import scrapy


class Item(scrapy.Item):
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    url = scrapy.Field()
    spider_name = scrapy.Field()
    market = scrapy.Field()
    retailer = scrapy.Field()
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    trail = scrapy.Field()
    skus = scrapy.Field()
