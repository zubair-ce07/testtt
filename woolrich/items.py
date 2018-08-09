import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    style_number = scrapy.Field()
    brand = scrapy.Field()
    colors = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    trail = scrapy.Field()
    categories = scrapy.Field()
    description = scrapy.Field()
    features = scrapy.Field()
    requests_queue = scrapy.Field()
    skus = scrapy.Field()
