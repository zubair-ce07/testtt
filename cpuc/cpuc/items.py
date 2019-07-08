# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy import Field


class DocumentDetail(scrapy.Item):
    filling_date = scrapy.Field()
    filled_by = scrapy.Field()
    description = scrapy.Field()
    document_type = scrapy.Field()
    document_link = scrapy.Field()
    proceeding_url = scrapy.Field()
    documents = scrapy.Field()


# class Document(scrapy.Item):
#     title = scrapy.Field()
#     link = scrapy.Field()
#     type = scrapy.Field()
#     date = scrapy.Field()


class File(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()


class ProceedingDetail(scrapy.Item):
    title = Field(output_processor=TakeFirst())
    filing_parties = Field()
    industries = Field()
    filled_on = Field(output_processor=TakeFirst())
    proceeding_type = Field(output_processor=TakeFirst())
    status = Field(output_processor=TakeFirst())
    description = Field(output_processor=TakeFirst())
    assignees = Field()
    filings = Field(default=[])
    source_url = Field(output_processor=TakeFirst())


class Filing(scrapy.Item):
    description = Field(output_processor=TakeFirst())
    documents = Field()
    filled_on = Field(output_processor=TakeFirst())
    filing_parties = Field()
    types = Field()


class Document(scrapy.Item):
    title = Field()
    source_url = Field()
    extension = Field()



