import scrapy


class SearsItem(scrapy.Item):
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()
    brand = scrapy.Field()
