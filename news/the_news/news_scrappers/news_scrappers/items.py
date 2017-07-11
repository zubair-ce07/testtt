# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import Join
from processors import CleanDate, StripString


class NewsScrappersItem(scrapy.Item):
    title = scrapy.Field(output_processor=StripString(),)
    date = scrapy.Field(output_processor=CleanDate(),)
    url = scrapy.Field(output_processor=StripString(),)
    img_url = scrapy.Field(output_processor=StripString(),)
    abstract = scrapy.Field(output_processor=StripString(),)
    detail = scrapy.Field(output_processor=Join('\n'),)
