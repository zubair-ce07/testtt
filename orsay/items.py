import scrapy


class OrsayItem(scrapy.Item):
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    skus = scrapy.Field()
    img_urls = scrapy.Field()

