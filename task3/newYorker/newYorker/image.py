from scrapy import Field, Item


class NewyorkerItemsVariantsImage(Item):
    key = Field()
    type = Field()
    angle = Field()
    has_thumbnail = Field()
    position = Field()
