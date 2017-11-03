import scrapy


class FarnellItem(scrapy.Item):
    url = scrapy.Field()
    brand = scrapy.Field()
    title = scrapy.Field()
    unit_price = scrapy.Field()
    overview = scrapy.Field()
    information = scrapy.Field()
    manufacturer = scrapy.Field()
    manufacturer_part = scrapy.Field()
    tariff_number = scrapy.Field()
    origin_country = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()
    image_urls = scrapy.Field()
    primary_image_url = scrapy.Field()
    trail = scrapy.Field()
