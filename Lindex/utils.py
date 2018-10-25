import re

from lindex.items import LindexItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


def clean_text(self, description):
    return [re.sub('\s+', ' ', text).strip() for text in description if text.strip()]


def clean_category(self, text):
    return text[0].split('/')


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
    pricing_details_out = TakeFirst()
