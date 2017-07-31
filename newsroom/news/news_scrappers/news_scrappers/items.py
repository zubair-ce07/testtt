# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import Join

from news.news_scrappers.news_scrappers.processors import CleanDate, StripString, StripStringTakeFirst


class NewsScrappersItem(scrapy.Item):
    title = scrapy.Field(output_processor=StripStringTakeFirst(),)
    published_date = scrapy.Field(output_processor=CleanDate(),)
    source_url = scrapy.Field(output_processor=StripStringTakeFirst(),)
    image_url = scrapy.Field(output_processor=StripStringTakeFirst(),)
    abstract = scrapy.Field(output_processor=StripString(),)
    detail = scrapy.Field(output_processor=Join('\n'),)
    category = scrapy.Field(output_processor=StripString(),)
    news_source = scrapy.Field(output_processor=StripString(),)
