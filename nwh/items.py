from urllib.parse import urljoin

import scrapy
from scrapy.loader.processors import MapCompose, Join


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
    image_url = scrapy.Field(
        input_processor=MapCompose(lambda url: urljoin('https://www.nwh.org', url))
    )
    address = scrapy.Field(
        output_processor=Join()
    )
    speciality = scrapy.Field(
        input_processor=MapCompose(filter_speciality)
    )
