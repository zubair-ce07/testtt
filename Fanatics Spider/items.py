import scrapy


class FanaticsItem(scrapy.Item):
    id = scrapy.Field()
    breadcrumb = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    categories = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    gender = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    language = scrapy.Field()
