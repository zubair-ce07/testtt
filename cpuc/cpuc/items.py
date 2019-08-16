"""Cpuc items module.

This is Cpuc items module.
"""
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Compose

clean_proceeding_no = Compose(
    lambda p: p[0].split('-')[0].strip())
clean_title = Compose(
    lambda p: re.sub(re.compile(r'<[^>]+>'), '', p[0]))


class Proceeding(scrapy.Item):
    """Proceeding Cpuc.

    Proceeding item class
    """

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
    """Proceeding Item loader.

    proceeding Item loader class
    """

    default_item_class = Proceeding
    default_output_processor = TakeFirst()
    proceeding_no_out = clean_proceeding_no
    documents_out = Identity()


class ProceedingDocument(scrapy.Item):
    """Proceeding Document.

    Proceeding Document Item class
    """

    filling_date = scrapy.Field()
    document_type = scrapy.Field()
    filed_by = scrapy.Field()
    description = scrapy.Field()
    files = scrapy.Field()
    link = scrapy.Field()


class ProceedingDocumentLoader(ItemLoader):
    """Proceeding document Item loader.

    proceeding document Item loader class
    """

    default_item_class = ProceedingDocument
    default_output_processor = TakeFirst()
    proceeding_no_out = clean_proceeding_no
    files_out = Identity()


class Document(scrapy.Item):
    """Document item.

    Document item Item class
    """

    title = scrapy.Field()
    doc_type = scrapy.Field()
    pdf_link = scrapy.Field()
    published_date = scrapy.Field()


class DocumentLoader(ItemLoader):
    """Proceeding item Item loader.

    Document item Item loader class
    """

    default_item_class = Document
    default_output_processor = TakeFirst()
    title_out = clean_title
