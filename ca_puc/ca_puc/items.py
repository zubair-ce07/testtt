# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from scrapy.loader.processors import MapCompose, TakeFirst, Identity


class CaPucItem(Item):
    filed_on = Field(output_processor=TakeFirst())
    assignees = Field(output_processor=TakeFirst())
    industries = Field(output_processor=TakeFirst())
    filed_by = Field(output_processor=TakeFirst())
    proceeding_type = Field(output_processor=TakeFirst())
    title = Field(output_processor=TakeFirst())
    status = Field(output_processor=TakeFirst())
    state_id = Field(
        input_processor=MapCompose(
            # x is heading "ID - 'Documets'"
            lambda x: x.split('-')[0],
            str.strip
        ),
        output_processor=TakeFirst()
    )
    filings = Field()
