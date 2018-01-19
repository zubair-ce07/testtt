import scrapy


class WoolworthCoItem(scrapy.Item):
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    brand = scrapy.Field()
    categories = scrapy.Field()
    details = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
