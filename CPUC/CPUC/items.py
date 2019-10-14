"""CPUC Items Module.

Module to initialize items and
itemloaders.
"""
import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst


class Proceeding(scrapy.Item):
    """Proceeding Item.

    Proceeding item class
    to initialize scrapy fields.
    """

    proceeding_number = scrapy.Field()
    filed_by = scrapy.Field()
    service_lists = scrapy.Field()
    industry = scrapy.Field()
    filing_date = scrapy.Field()
    category = scrapy.Field()
    current_status = scrapy.Field()
    description = scrapy.Field()
    staff = scrapy.Field()
    documents = scrapy.Field()
    total_documents = scrapy.Field()

class ProceedingLoader(ItemLoader):
    """Proceeding Item loader.

    Proceeding Item loader class
    to input proceeding item.
    """

    default_item_class = Proceeding
    default_output_processor = TakeFirst()
    documents_out = Identity()


class ProceedingDocument(scrapy.Item):
    """Proceeding Document.

    Proceeding Document Item class
    to initialize proceeding document's
    scrapy fields.
    """

    document_filing_date = scrapy.Field()
    document_type = scrapy.Field()
    filed_by = scrapy.Field()
    description = scrapy.Field()
    files = scrapy.Field()
    document_url = scrapy.Field()


class ProceedingDocumentLoader(ItemLoader):
    """Proceeding document Item loader.

    Proceeding document Item loader class
    to input proceeding document item.
    """

    default_item_class = ProceedingDocument
    default_output_processor = TakeFirst()
    files_out = Identity()


class Document(scrapy.Item):
    """Document item.

    Document item class to
    initialize document data
    scrapy fields.
    """

    title = scrapy.Field()
    doc_type = scrapy.Field()
    pdf_link = scrapy.Field()
    published_date = scrapy.Field()


class DocumentLoader(ItemLoader):
    """Proceeding item loader.

    Document item loader class to
    input Documnet item.
    """

    default_item_class = Document
    default_output_processor = TakeFirst()
