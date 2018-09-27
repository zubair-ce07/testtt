import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, MapCompose
from w3lib.html import remove_tags


class WalmartItem(scrapy.Item):
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()


class WalmartLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = WalmartItem
    description_in = MapCompose(remove_tags)
    name_out = Join()
