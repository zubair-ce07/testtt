import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


def filter_image_url(value):
    value = value[1:]
    value = "http://www.greatfoodhall.com/eshop" + value
    return value


def filter_categories(value):
    value = value.strip()
    return value


class GreatfoodhallItem(scrapy.Item):
    name = scrapy.Field()
    brand= scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    availability = scrapy.Field()
    unit = scrapy.Field()
    image_url = scrapy.Field()
    page_url = scrapy.Field()
    reviews_score = scrapy.Field()
    barcode = scrapy.Field()
    price = scrapy.Field()
    discounted_price = scrapy.Field()


class GreatfoodhallLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = GreatfoodhallItem
    categories_in = MapCompose(remove_tags, filter_categories)
    image_url_in = MapCompose(filter_image_url)


