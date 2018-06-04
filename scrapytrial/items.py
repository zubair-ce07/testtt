import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose


def remove_artist(value):
    return value.strip("Artist: ")


def remove_trailing_line(values):
    return [x.strip() for x in values]


def clean_space(values):
    return list(filter(None, values))


class ScrapyTrialItem(scrapy.Item):
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    artist = scrapy.Field(
        input_processor=MapCompose(remove_artist),
    )
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    image = scrapy.Field(
        output_processor=TakeFirst()
    )
    height = scrapy.Field(
        output_processor=TakeFirst()
    )
    width = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=Compose(remove_trailing_line, clean_space),
        output_processor=Join(", ")
    )
    path = scrapy.Field()

