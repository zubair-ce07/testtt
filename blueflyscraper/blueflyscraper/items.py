import scrapy


class BlueflyItem(scrapy.Item):
    product_id = scrapy.Field()
    merch_info = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    product_title = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    skus = scrapy.Field()


class SkuItem(scrapy.Item):
    colour = scrapy.Field()
    price = scrapy.Field()
    previous_prices = scrapy.Field()
    size = scrapy.Field()
