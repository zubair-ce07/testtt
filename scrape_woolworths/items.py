import scrapy


class WoolWorthsItem(scrapy.Item):
    brand = scrapy.Field()
    retailer_sku = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()

