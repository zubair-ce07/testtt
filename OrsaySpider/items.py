import scrapy


class OrsayspiderItem(scrapy.Item):
    brand = scrapy.Field(default='Osray')
    care = scrapy.Field()
    category = scrapy.Field(default=[])
    description = scrapy.Field()
    gender = scrapy.Field(default='women')
    image_urls = scrapy.Field()
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    url_original = scrapy.Field()

