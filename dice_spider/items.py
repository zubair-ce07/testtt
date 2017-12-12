import scrapy

class Job(scrapy.Item):
    categories = scrapy.Field()
    company = scrapy.Field()
    company_url = scrapy.Field()
    description = scrapy.Field()
    external_id = scrapy.Field()
    job_date = scrapy.Field()
    job_types = scrapy.Field()
    location = scrapy.Field()
    logo_urls = scrapy.Field()
    provider = scrapy.Field()
    salary = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
