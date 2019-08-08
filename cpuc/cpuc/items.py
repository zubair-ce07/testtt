# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose
import re

clean_proceeding_no = Compose(
    lambda p: p[0].split('-')[0].strip())
clean_title = Compose(
    lambda p: re.sub(re.compile(r'<[^>]+>'), '', p[0]))


class Proceeding(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    proceeding_no = scrapy.Field()
    filed_by = scrapy.Field()
    service_list = scrapy.Field()
    industry = scrapy.Field()
    filling_date = scrapy.Field()
    category = scrapy.Field()
    current_status = scrapy.Field()
    description = scrapy.Field()
    staff = scrapy.Field()
    documents = scrapy.Field()
    total_documents = scrapy.Field()


class ProceedingLoader(ItemLoader):
    default_item_class = Proceeding
    default_output_processor = TakeFirst()
    proceeding_no_out = clean_proceeding_no
    # filed_by_out = Identity()
    # service_list_out = Identity()
    # industry_out = Identity()
    # filling_date_out = Identity()
    # category = Identity()
    # current_status_out = Identity()
    # description_out = Identity()
    # staff_out = Identity()
    documents_out = Identity()
    # total_documents_in = TakeFirst()


class ProceedingDocument(scrapy.Item):
    filling_date = scrapy.Field()
    document_type = scrapy.Field()
    filed_by = scrapy.Field()
    description = scrapy.Field()
    files = scrapy.Field()
    link = scrapy.Field()


class ProceedingDocumentLoader(ItemLoader):
    default_item_class = ProceedingDocument
    default_output_processor = TakeFirst()
    proceeding_no_out = clean_proceeding_no
    files_out = Identity()


class Document(scrapy.Item):
    title = scrapy.Field()
    doc_type = scrapy.Field()
    pdf_link = scrapy.Field()
    published_date = scrapy.Field()


class DocumentLoader(ItemLoader):
    default_item_class = Document
    default_output_processor = TakeFirst()
    title_out = clean_title
