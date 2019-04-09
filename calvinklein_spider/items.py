import scrapy


class CalvinkleinSpiderItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    care = scrapy.Field()
    lang = scrapy.Field()
    skus = scrapy.Field()
    brand = scrapy.Field()
    gender = scrapy.Field()
    market = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
