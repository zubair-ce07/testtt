
import scrapy


class TopshopItem(scrapy.Item):

    category = scrapy.Field()
    retailer_sku = scrapy.Field()
    merch_info = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url_original = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    spider_name = scrapy.Field()
    retailer = scrapy.Field()
    market = scrapy.Field()
    currency = scrapy.Field()
