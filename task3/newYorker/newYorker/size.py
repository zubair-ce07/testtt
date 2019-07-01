from scrapy import Field, Item


class NewyorkerItemsVariantsSize(Item):
    size_value = Field()
    size_name = Field()
    bar_code = Field()
