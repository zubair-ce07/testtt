import scrapy
import re

from scrapy.loader.processors import TakeFirst, Join, MapCompose, Compose
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class BizzbyItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    company_name = scrapy.Field()
    contact_name = scrapy.Field()
    postcode = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    services = scrapy.Field()
    products = scrapy.Field()
    notes = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    telephone = scrapy.Field()
    gas_safe_number = scrapy.Field()
    about_us = scrapy.Field()
    areas_of_expertise = scrapy.Field()
    number_of_reviews = scrapy.Field()
    average_rating = scrapy.Field()
    review_content = scrapy.Field()
    categories = scrapy.Field()
    keywords = scrapy.Field()
    open_hours = scrapy.Field()
    search_postcode = scrapy.Field()
    search_keyword = scrapy.Field()
    search_category = scrapy.Field()


class YellowPagesItem(BizzbyItem):
    associations = scrapy.Field()
    specialties = scrapy.Field()


def _remove_empty(loader, values):
    return [x for x in values if x]


class BizzbyItemLoader(ItemLoader):
    default_item_class = YellowPagesItem
    default_input_processor = lambda loader, values: [x.strip() for x in values]
    default_output_processor = TakeFirst()
    address_out = lambda loader, values: ', '.join(x for x in values if x)
    telephone_out = _remove_empty
    services_out = _remove_empty
    products_out = _remove_empty
    areas_of_expertise = _remove_empty
    about_us_out = lambda loader, values: ' '.join(x for x in values if x)
    categories_out = _remove_empty
    keywords_out = _remove_empty
    # this is definitely not good enough. but the customer requires strictly CSV
    review_content_out = lambda loader, values: ' | '.join(x for x in values if x)


def clean_space(value):
    return re.sub("\s+", " ", value)


def _strip_more_less(value):
    return clean_space(value.strip(",more... less..."))


class YellowPagesLoader(BizzbyItemLoader):
    telephone_out = TakeFirst()
    address_out = Join()

    services_out = Compose(Join(""), lambda x: x.strip("Services"), _strip_more_less)
    services_in = MapCompose(remove_tags, clean, clean_space)

    products_out = Compose(Join(""), lambda x: x.strip("Products and Services"), _strip_more_less)
    products_in = MapCompose(remove_tags, clean, clean_space)

    associations_out = Compose(Join(""), lambda x: x.strip("Associations"), _strip_more_less)
    associations_in = MapCompose(remove_tags, clean, clean_space)

    specialties_out = Compose(Join(""), lambda x: x.strip("Specialties"), _strip_more_less)
    specialties_in = MapCompose(remove_tags, clean, clean_space)

    average_rating_in = MapCompose(remove_tags)
    average_rating_out = TakeFirst()

    review_content_in = MapCompose(remove_tags, Join(""), clean_space)

