import scrapy


class DoctorProfile(scrapy.Item):
    crawled_date = scrapy.Field()
    gender = scrapy.Field()
    specialty = scrapy.Field()
    source_url = scrapy.Field()
    image_url = scrapy.Field()
    languages = scrapy.Field()
    affiliation = scrapy.Field()
    medical_school = scrapy.Field()
    statement = scrapy.Field()
    full_name = scrapy.Field()
    address = scrapy.Field()
    graduate_education = scrapy.Field()
