import scrapy
from scrapy.loader.processors import Identity


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field(output_processor=Identity())
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    market = scrapy.Field()
    url_original = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field(output_processor=Identity())
    skus = scrapy.Field(output_processor=Identity())
