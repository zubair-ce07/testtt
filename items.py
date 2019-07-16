import scrapy


class BeyondLimitItem(scrapy.Field):
    name = scrapy.Field(),
    size = scrapy.Field(),
    gender = scrapy.Field(),
    description = scrapy.Field(),
    retailer_sku = scrapy.Field(),
    image = scrapy.Field(),
    care = scrapy.Field(),
    url = scrapy.Field(),
    lang = scrapy.Field(),
    brand = scrapy.Field(),
    category = scrapy.Field(),
    skus = scrapy.Field()
    pass
