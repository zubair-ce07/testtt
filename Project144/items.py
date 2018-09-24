# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from w3lib.html import remove_tags
from scrapy.loader.processors import Join, MapCompose, TakeFirst


class Item(scrapy.Item):
    Type = scrapy.Field()
    zip_code = scrapy.Field()
    address = scrapy.Field()
    Zugangszeiten = scrapy.Field()
    Wegbeschreibung = scrapy.Field()
    Wo_genau_ist_der_Defi_angebracht = scrapy.Field()
    Erreichbarkeit_von_der_Straße = scrapy.Field()


def filter_zip_code(self, value):
    value = value[0]
    return re.findall('\d+', value)


def filter_address(self, value):
    value = value[0]
    return value.replace(re.findall('\d+', value)[0], '').strip()


def filter_Zugangszeiten(self, value):
    if 0 < len(value):
        return value[0].strip()
    else:
        return ""


def filter_Wegbeschreibung(self, value):
    if 1 < len(value):
        return value[1].strip()
    else:
        return ""


def filter_Wo_genau(self, value):
    if 2 < len(value):
        return value[2].strip()
    else:
        return ""


def filter_Erreichbarkeit(self, value):
    if 3 < len(value):
        return value[3].strip()
    else:
        return ""


class ItemLoader(scrapy.loader.ItemLoader):
    Type_out = TakeFirst()
    zip_code_in = filter_zip_code
    zip_code_out = TakeFirst()
    address_in = filter_address
    address_out = TakeFirst()
    Zugangszeiten_in = filter_Zugangszeiten
    Zugangszeiten_out = TakeFirst()
    Wegbeschreibung_in = filter_Wegbeschreibung
    Wegbeschreibung_out = TakeFirst()
    Wo_genau_ist_der_Defi_angebracht_in = filter_Wo_genau
    Wo_genau_ist_der_Defi_angebracht_out = TakeFirst()
    Erreichbarkeit_von_der_Straße_in = filter_Erreichbarkeit
    Erreichbarkeit_von_der_Straße_out = TakeFirst()
