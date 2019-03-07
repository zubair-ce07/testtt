from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import Join
from scrapy.loader.processors import TakeFirst

from nwh.items import DoctorItem
from nwh.items import AddressItem


def strip(value):
    return value.strip()


map_strip = MapCompose(strip)
clean_text = Compose(map_strip, Join(), strip)
name_dict = MapCompose(lambda name: {'name': name})


class DoctorItemLoader(ItemLoader):
    default_item_class = DoctorItem
    full_name_out = TakeFirst()
    specialty_out = Compose(TakeFirst(), lambda str: str.split(','), map_strip)
    image_url_out = TakeFirst()
    source_url_out = TakeFirst()
    crawled_date_out = TakeFirst()
    graduate_education_out = MapCompose(
        lambda name: {'type': 'Residency', 'name': name})
    medical_school_out = name_dict
    affiliation_out = name_dict


class AddressItemLoader(ItemLoader):
    default_item_class = AddressItem
    phone_out = clean_text
    fax_out = clean_text
