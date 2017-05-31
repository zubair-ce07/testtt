import scrapy


class SheegoSpiderItem(scrapy.Item):
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    url_original = scrapy.Field()
