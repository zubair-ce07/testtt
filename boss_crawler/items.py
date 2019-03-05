import scrapy


class BossCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    lang = scrapy.Field()
    skus = scrapy.Field()
    meta = scrapy.Field()
    care = scrapy.Field()
    brand = scrapy.Field()
    gender = scrapy.Field()
    market = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
