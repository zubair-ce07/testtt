import scrapy


class UrbanLockerItem(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()
    retailer_sku = scrapy.Field()
    image_urls = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    currency = scrapy.Field()
