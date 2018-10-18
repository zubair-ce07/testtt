import re

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


class LindexItem(Item):
    uuid = Field()
    brand = Field()
    care = Field()
    category = Field()
    description = Field()
    gender = Field()
    image_urls = Field()
    name = Field()
    price = Field()
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
    currency = Field()
    spider_name = Field()
    crawl_start_time = Field()


def clean_text(self, description):
    return [re.sub('\s+', ' ', text).strip() for text in description if text.strip()]


def clean_category(self, text):
    return text[0].split('/')


def find_currency(self, text):
    return "".join(re.findall(r"[^\d. ]", text[0]))


class LindexItemLoader(ItemLoader):
    default_item_class = LindexItem
    uuid_out = TakeFirst()
    industry_out = TakeFirst()
    name_out = TakeFirst()
    price_out = TakeFirst()
    spider_name_out = TakeFirst()
    retailer_sku_out = TakeFirst()
    url_orignal_out = TakeFirst()
    url_out = TakeFirst()
    brand_out = TakeFirst()
    market_out = TakeFirst()
    retailer_out = TakeFirst()
    date_out = TakeFirst()
    crawl_id_out = TakeFirst()
    currency_in = find_currency
    currency_out = TakeFirst()
    gender_out = TakeFirst()
    crawl_start_time_out = TakeFirst()
    category_in = clean_category
    description_in = clean_text
    care_in = clean_text
