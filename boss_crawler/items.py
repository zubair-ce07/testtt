import scrapy


class BossCrawlerItem(scrapy.Item):
    name = scrapy.Field()
    lang = scrapy.Field()
    brand = scrapy.Field()
    gender = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    market = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    meta = scrapy.Field()
