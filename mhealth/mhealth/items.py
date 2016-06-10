import scrapy


class DoctorProfile(scrapy.Item):
    crawled_date = scrapy.Field()
    affiliation = scrapy.Field()
    specialty = scrapy.Field()
    source_url = scrapy.Field()
    languages = scrapy.Field()
    clinical_interest = scrapy.Field()
    medical_school = scrapy.Field()
    image_url = scrapy.Field()
    full_name = scrapy.Field()
    address = scrapy.Field()
    graduate_education = scrapy.Field()
