import scrapy
import re

from scrapy.loader.processors import TakeFirst, Join, MapCompose, Compose
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class degulesiderItemLoader(BizzbyItemLoader):
    telephone_out = TakeFirst()
    categories_out = TakeFirst()

