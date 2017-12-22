from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst
import scrapy


class Job(scrapy.Item):
    category = scrapy.Field()
    crawled_at = scrapy.Field()
    description = scrapy.Field()
    job_id = scrapy.Field()
    job_date = scrapy.Field()
    job_url = scrapy.Field()
    job_type = scrapy.Field()
    locations = scrapy.Field()
    provider = scrapy.Field()
    title = scrapy.Field()


class JobLoader(ItemLoader):
    default_item_class = Job
    default_output_processor = TakeFirst()
    locations_out = Compose()
