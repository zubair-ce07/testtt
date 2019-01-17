import scrapy


class OrsayCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    lang = scrapy.Field()
    care = scrapy.Field()
    name = scrapy.Field()
    skus = scrapy.Field()
    meta = scrapy.Field()
    brand = scrapy.Field()
    market = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
