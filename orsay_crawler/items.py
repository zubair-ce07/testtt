import scrapy


class OrsayCrawlerItem(scrapy.Item):
    lang = scrapy.Field()
    market = scrapy.Field()
    gender = scrapy.Field()
    url = scrapy.Field()
    care = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    meta = scrapy.Field()
