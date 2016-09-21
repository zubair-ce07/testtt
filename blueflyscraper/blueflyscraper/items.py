import scrapy


class BlueflyItem(scrapy.Item):
    product_id = scrapy.Field()
    merch_info = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()

