import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, Join, TakeFirst
from urlparse import urljoin


def process_str(result):
    if result:
        return result[0].strip().replace(' ', '').split(',')

def process_company_url(result):
    return urljoin('https://www.dice.com', result[0])

def process_logo_url(result):
    if result:
        return urljoin('https:', result[0])

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
    categories_out = Compose(process_str)
    company_url_out = Compose(process_company_url)
    description_out = Join()
    job_types_out = Compose(process_str)
    logo_urls_out = Compose(process_logo_url)
