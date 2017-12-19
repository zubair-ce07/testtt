import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, Join, TakeFirst


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


class JobLoader(ItemLoader):
    default_item_class = Job
    default_output_processor = TakeFirst()
    categories_out = Compose()
    description_out = Join()
    job_types_out = Compose()
    logo_urls_out = Compose()
