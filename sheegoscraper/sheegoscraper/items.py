import scrapy


class SheegoItem(scrapy.Item):
    brand = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    name = scrapy.Field()
    product_id = scrapy.Field()
    url_original = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()
    category = scrapy.Field()
    pass
