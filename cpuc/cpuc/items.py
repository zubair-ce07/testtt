import scrapy
from scrapy.loader.processors import TakeFirst
from scrapy import Field


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
