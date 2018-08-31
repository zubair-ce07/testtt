# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CaseProceeding(scrapy.Item):
    # define the fields for your item here like:
    number = scrapy.Field()
    filed_by = scrapy.Field(serializer=list)
    industry = scrapy.Field(serializer=list)
    filing_date = scrapy.Field()
    category = scrapy.Field(serializer=list)
    status = scrapy.Field()
    description = scrapy.Field()
    staff_members = scrapy.Field(serializer=list)
    documents = scrapy.Field(serializer=list)


# class Staff(scrapy.Item):
#     designation = scrapy.Field()
#     name = scrapy.Field()
#     assign_date = scrapy.Field()

class ProceedingDocument(scrapy.Item):
    filing_date = scrapy.Field()
    type = scrapy.Field()
    filed_by = scrapy.Field()
    description = scrapy.Field()
    document_files = scrapy.Field(serializer=list)


class ProceedingFile(scrapy.Item):
    title = scrapy.Field()
    type = scrapy.Field()
    file_url = scrapy.Field()
    date_published = scrapy.Field()
    related_proceedings = scrapy.Field(serializer=list)
