import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst


class Job(scrapy.Item):
    business_area = scrapy.Field()
    crawled_at = scrapy.Field()
    description = scrapy.Field()
    experience_level = scrapy.Field()
    job_date = scrapy.Field()
    job_function = scrapy.Field()
    location = scrapy.Field()
    provider = scrapy.Field()
    provider_url = scrapy.Field()
    requisition_no = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()


class JobLoader(ItemLoader):
    default_item_class = Job
    default_output_processor = TakeFirst()
    description_out = Join()
