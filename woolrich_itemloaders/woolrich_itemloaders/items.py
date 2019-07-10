import re
import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst

def split_price(price):
    return float(re.match(r'(\W+)(\d*[,]*\d*[.]*\d*)', price).group(2).replace(',', ''))

def split_currency(price):
    return re.match(r'(\W+)(\d*[,]*\d*[.]*\d*)', price).group(1)

def get_gender(categories):
    return "Men" if "Men" in categories else "Women" if "Women" in categories else "Unisex"

class Product(scrapy.Item):
    retailer_sku = scrapy.Field()
    lang = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()

class Sku(scrapy.Item):
    price = scrapy.Field()
    currency = scrapy.Field()
    previous_price = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    availability = scrapy.Field()
    
class ProductLoader(ItemLoader):
    default_item_class = Product
    default_output_processor = TakeFirst()
    category_out = Identity()
    desc_out = Identity()
    care_out = Identity()
    image_urls_out = Identity()
    gender_in = MapCompose(get_gender)
    price_in = MapCompose(split_price)
    currency_in = MapCompose(split_currency)

class SkuLoader(ItemLoader):
    default_item_class = Sku
    default_output_processor = TakeFirst()
    price_in = MapCompose(split_price)
    currency_in = MapCompose(split_currency)
