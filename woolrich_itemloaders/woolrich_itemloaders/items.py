import re
import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

def split_price(price):
    return float(re.match(r'(\W+)(\d*[,]*\d*[.]*\d*)', price).group(2).replace(',', ''))

def split_currency(price):
    return re.match(r'(\W+)(\d*[,]*\d*[.]*\d*)', price).group(1)

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
    
    retailer_sku_out = TakeFirst()
    lang_out = TakeFirst()
    gender_out = TakeFirst()
    url_out = TakeFirst()
    date_out = TakeFirst()
    market_out = TakeFirst()
    name_out = TakeFirst()
    skus_out = TakeFirst()
    price_out = TakeFirst()
    price_in = MapCompose(split_price)
    currency_out = TakeFirst()
    currency_in = MapCompose(split_currency)

class SkuLoader(ItemLoader):
    default_item_class = Sku

    price_out = TakeFirst()
    price_in = MapCompose(split_price)
    currency_out = TakeFirst()
    currency_in = MapCompose(split_currency)
    previous_price_out = TakeFirst()
    color_out = TakeFirst()
    size_out = TakeFirst()
    availability_out = TakeFirst()
