# -*- coding: utf-8 -*-
from scrapy import Item, Field


class NwhscrapperItem(Item):
    crawled_date = Field()
    speciality = Field()
    source_url = Field()
    affiliation = Field()
    medical_school = Field()
    image_url = Field()
    full_name = Field()
    address = Field()
    graduate_education = Field()
