# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
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
    title = Field()
    filing_parties = Field()
    industries = Field()
    filled_on = Field()
    proceeding_type = Field()
    status = Field()
    description = Field()
    assignees = Field()
    filings = Field()
    source_url = Field()


class Filing(scrapy.Item):
    description = Field()
    documents = Field()
    filled_on = Field()
    filing_parties = Field()
    types = Field()


class Document(scrapy.Item):
    title = Field()
    source_url = Field()
    extension = Field()