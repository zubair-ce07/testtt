# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose


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


class RunningBareItem(scrapy.Item):
    brand = scrapy.Field(
        output_processor=TakeFirst()
    )
    care = scrapy.Field()
    currency = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field()
    gender = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_urls = scrapy.Field()
    industry = scrapy.Field(
        output_processor=TakeFirst()
    )
    market = scrapy.Field(
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        output_processor=TakeFirst()
    )
    retailer = scrapy.Field(
        output_processor=TakeFirst()
    )
    retailer_sku = scrapy.Field(
        output_processor=TakeFirst()
    )
    skus = scrapy.Field(
        output_processor=TakeFirst()
    )
    spider_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    url_original = scrapy.Field(
        output_processor=TakeFirst()
    )


class SheegoItem(scrapy.Item):
    brand = scrapy.Field(
        output_processor=Compose(lambda brands: brands[0], str.upper)
    )
    care = scrapy.Field(
        output_processor=TakeFirst()
    )
    category = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_urls = scrapy.Field()
    lang = scrapy.Field(
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    retailer_sku = scrapy.Field(
        output_processor=TakeFirst()
    )
    skus = scrapy.Field(
        output_processor=TakeFirst()
    )
    oos_request = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    url_original = scrapy.Field(
        output_processor=TakeFirst()
    )
