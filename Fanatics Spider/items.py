import scrapy


class FanaticsItem(scrapy.Item):
    product_id = scrapy.Field()
    breadcrumb = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    categories = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    gender = scrapy.Field()
    product_url = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    language = scrapy.Field()
