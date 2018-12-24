# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class Item(scrapy.Item):
    categories=scrapy.Field()
    company=scrapy.Field()
    crawled_at=scrapy.Field()
    description=scrapy.Field(output_processor=TakeFirst())
    external_id=scrapy.Field(output_processor=TakeFirst())
    job_date=scrapy.Field()
    job_types=scrapy.Field()
    location=scrapy.Field(output_processor=TakeFirst())
    logo_urls=scrapy.Field()
    provider=scrapy.Field(output_processor=TakeFirst())
    title=scrapy.Field(output_processor=TakeFirst())
    url=scrapy.Field(output_processor=TakeFirst())
