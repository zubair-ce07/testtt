import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst

def make_list(result):
    return result[0].strip().split(",")


def process_description(result):
    return ''.join(result).strip()


def process_fellowship_organization(result):
    return result[0].strip()


class Fellowship(scrapy.Item):
    crawled_at = scrapy.Field()
    deadline = scrapy.Field()
    description = scrapy.Field()
    disciplines = scrapy.Field()
    experience = scrapy.Field()
    external_id = scrapy.Field()
    fellowship_organization = scrapy.Field()
    fellowship_url = scrapy.Field()
    keywords = scrapy.Field()
    location = scrapy.Field()
    provider = scrapy.Field()
    site_record_url = scrapy.Field()
    title = scrapy.Field()


class FellowshipLoader(ItemLoader):
    default_item_class = Fellowship
    default_output_processor = TakeFirst()
    description_out = Compose(process_description)
    disciplines_out = Compose(make_list)
    fellowship_organization_out = Compose(process_fellowship_organization)
    keywords_out = Compose(make_list)
