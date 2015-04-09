import scrapy

class ZipCodeItem(scrapy.Item):
     county = scrapy.Field()
     city = scrapy.Field()
     state = scrapy.Field()
     counties = scrapy.Field()
     cities = scrapy.Field()