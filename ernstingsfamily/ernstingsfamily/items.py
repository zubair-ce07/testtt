import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    actual_price = scrapy.Field()
    discount_price = scrapy.Field()
    url = scrapy.Field()
    skus = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

class StoreKeepingUnits(scrapy.Item):
    sku_id = scrapy.Field()
    actual_price = scrapy.Field()
    discount_price = scrapy.Field()
    size = scrapy.Field()
    colour = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)