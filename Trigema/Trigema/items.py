# -*- coding: utf-8 -*-
from scrapy import Item, Field


class MarinaItem(Item):
    def __init__(self, *args, **kwargs):
        super(MarinaItem, self).__init__(*args, **kwargs)
        self['locality'] = u'Bubenské nábř 17000 Praha 7 Czechia'
        self['gps'] = {"latitude": "50.106281", "longitude": "14.458883"}
        self['finished'] = False
        self['energy_class'] = 'B'
        self['cellar'] = True
        self['ownership'] = 'private'
        self['project'] = 'Trigema Island'
        self['developer'] = 'Trigema Island inc.'
        self['type'] = 'flat'

    ownership = Field()
    project = Field()
    developer = Field()
    locality = Field()
    gps = Field()
    energy_class = Field()
    type = Field()
    finished = Field()
    cellar = Field()
    number = Field()
    local_id = Field()
    detail_url = Field()
    timestamp = Field()
    building = Field()
    floor = Field()
    disposition = Field()
    usable_area = Field()
    terrace = Field()
    storeroom = Field()
    state = Field()
    parking = Field()
    price = Field()
    price_excluding_vat = Field()
    orientation = Field()
    floor_area = Field()
    balcony = Field()
    indoor_garden = Field()
    garden = Field()
    room = Field()
