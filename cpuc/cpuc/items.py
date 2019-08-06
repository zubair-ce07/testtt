# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Proceeding(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    proceeding_no = scrapy.Field()
    filled_by = scrapy.Field()
    service_list = scrapy.Field()
    industry = scrapy.Field()
    filling_date = scrapy.Field()
    category = scrapy.Field()
    current_status = scrapy.Field()
    description = scrapy.Field()
    staff = scrapy.Field()
    documents = scrapy.Field()
    total_documents = scrapy.Field()


class ProceedingDocument(scrapy.Item):
    # filling_date = scrapy.Field()
    # document_type = scrapy.Field()
    # filled_by = scrapy.Field()
    # description = scrapy.Field()
    files = scrapy.Field()
    link = scrapy.Field()


class Document(scrapy.Item):
    title = scrapy.Field()
    doc_type = scrapy.Field()
    pdf_link = scrapy.Field()
    published_date = scrapy.Field()
