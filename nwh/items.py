from urllib.parse import urljoin

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst


def filter_speciality(value):
    filtered = value.strip()
    return filtered


class NwhItem(scrapy.Item):
    crawled_date = scrapy.Field()
    source_url = scrapy.Field()
    affiliation = scrapy.Field()
    medical_school = scrapy.Field()
    graduate_education = scrapy.Field()
    full_name = scrapy.Field()
    image_url = scrapy.Field()
    address = scrapy.Field()
    speciality = scrapy.Field()


class NwhLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = NwhItem
    image_url_in = MapCompose(lambda url: urljoin('https://www.nwh.org', url))
    address_out = Join()
    speciality_in = MapCompose(filter_speciality)
