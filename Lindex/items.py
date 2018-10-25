import re

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst
from lindex.utils import clean_category, clean_currency, clean_text


class LindexItem(Item):
    uuid = Field()
    brand = Field()
    care = Field()
    categories = Field()
    description = Field()
    gender = Field()
    image_urls = Field()
    name = Field()
    price = Field()
    currency = Field()
    retailer_sku = Field()
    skus = Field()
    url = Field()
    url_orignal = Field()
    market = Field()
    retailer = Field()
    date = Field()
    crawl_id = Field()
    industry = Field()
    product_hash = Field()
    spider_name = Field()
    crawl_start_time = Field()
    meta = Field()


class LindexItemLoader(ItemLoader):
    default_item_class = LindexItem
    uuid_out = TakeFirst()
    industry_out = TakeFirst()
    name_out = TakeFirst()
    spider_name_out = TakeFirst()
    retailer_sku_out = TakeFirst()
    url_orignal_out = TakeFirst()
    url_out = TakeFirst()
    brand_out = TakeFirst()
    market_out = TakeFirst()
    retailer_out = TakeFirst()
    date_out = TakeFirst()
    crawl_id_out = TakeFirst()
    gender_out = TakeFirst()
    crawl_start_time_out = TakeFirst()
    categories_in = clean_category
    description_in = clean_text
    care_in = clean_text
    currency_in = clean_currency
    currency_out = TakeFirst()
