from scrapy import Item, Field


class Docket(Item):
    filed_on = Field()    
    industries = Field()
    title = Field()
    state = Field()
    status = Field()
    filings = Field()
    source_url = Field()
    source_title = Field()
    assignees = Field()
    major_parties = Field()
