import scrapy
from scrapy.loader.processors import MapCompose

class FindadoctorItem(scrapy.Item):
    crawled_date = scrapy.Field()
    speciality = scrapy.Field(input_processor=MapCompose(unicode.strip))
    source_url  = scrapy.Field()
    affiliation = scrapy.Field()
    medical_school = scrapy.Field()
    image_url = scrapy.Field()
    full_name = scrapy.Field()
    address = scrapy.Field()
    graduate_education = scrapy.Field()
