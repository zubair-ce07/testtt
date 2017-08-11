# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class UpworkScrapyItem(scrapy.Item):
    crawled_at = scrapy.Field(serializer=str)
    url = scrapy.Field(serializer=str)
    categories = scrapy.Field()
    description = scrapy.Field()
    experience = scrapy.Field()
    job_types = scrapy.Field()
    provider = scrapy.Field()
    title = scrapy.Field()
    external_id = scrapy.Field(serializer=str)
    project_type = scrapy.Field()
    client_rating = scrapy.Field()
    client_reviews = scrapy.Field()
    job_posted_location = scrapy.Field()
    jobs_posted = scrapy.Field()
    hire_rate = scrapy.Field()
    budget = scrapy.Field()
    other_skills = scrapy.Field()


