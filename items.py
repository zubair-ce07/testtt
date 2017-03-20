# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class Job(scrapy.Item):
    crawled_at = scrapy.Field(
        output_processor=TakeFirst()
    )
    categories = scrapy.Field(
        input_processor=MapCompose(str.strip)
    )
    company = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    company_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join()
    )
    external_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_urls = scrapy.Field(
        output_processor=TakeFirst()
    )
    job_types = scrapy.Field(
        input_processor=MapCompose(str.strip)
    )
    job_date = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    location = scrapy.Field(
        output_processor=TakeFirst()
    )
    logo_urls = scrapy.Field(
        output_processor=TakeFirst()
    )
    provider = scrapy.Field(
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
