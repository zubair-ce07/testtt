from json import loads

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Compose


class ProductItem(Item):
    retailer_sku = Field()
    lang = Field()
    trail = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    date = Field()
    market = Field()
    url_original = Field()
    name = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
    out_of_stock = Field()
    price = Field()
    currency = Field()


def gender(gender_soup):
    gender_map = {
        "Men": "men",
        "Women": "women",
    }

    for gender in gender_map:
        if gender in gender_soup:
            return gender_map[gender]

    return "unisex"


def sku(response):
    raw_sku = loads(response.text)["data"]
    sku_price = raw_sku["price"]
    sku = {
        "colour": response.meta["colour"],
        "size": response.meta['size'],
        "price": int(sku_price["without_tax"]["value"] * 100),
        "currency": "USD"
    }

    if sku_price.get("rrp_without_tax"):
        sku["previous_prices"] = [int(sku_price["rrp_without_tax"]["value"] * 100)]

    if not raw_sku["instock"]:
        sku["out_of_stock"] = True

    return {raw_sku["sku"]: sku}


class ProductItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

    retailer_sku_in = MapCompose(lambda sku: sku.split('#: ')[1])
    trail_out = Identity()
    gender_in = Compose(gender)
    category_out = Identity()
    description_out = Identity()
    care_out = Identity()
    image_urls_out = Identity()
    skus_out = Identity()
