# -*- coding: utf-8 -*-
# Define here the models for your scraped items
from scrapy import Item, Field


class Student(Item):
    roll_no = Field()
    name = Field()
    father_name = Field()
    score = Field()

# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
