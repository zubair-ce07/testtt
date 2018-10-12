import scrapy


class OrsayItem(scrapy.Item):
    brand = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    colors_queue = scrapy.Field()
