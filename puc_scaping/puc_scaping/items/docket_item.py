""" Items related to docket """
from scrapy import Item
from scrapy import Field


class DocketItem(Item):
    """Docket Item"""
    assignees = Field()
    filings = Field()
    filed_on = Field()
    industries = Field()
    major_parties = Field()
    matter_id = Field()
    proceeding_sub_type = Field()
    proceeding_type = Field()
    source_url = Field()
    state = Field()
    state_id = Field()
    status = Field()
    title = Field()


class FilingItem(Item):
    """Filig items with docuements details to be used in docket item"""
    description = Field()
    documents = Field()
    filed_on = Field()
    filing_parties = Field()
    slug = Field()
    source_filing_parties = Field()
    state_id = Field()
    types = Field()


class DocumentItem(Item):
    """Document item to be used in Filing item"""
    blob_name = Field()
    extension = Field()
    name = Field()
    onS3 = Field()
    slug = Field()
    source_url = Field()
    title = Field()
