import scrapy


class BlueflyItem(scrapy.Item):
    brand = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    merch_info = scrapy.Field()
    name = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    url_original = scrapy.Field()
