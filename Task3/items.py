import scrapy
from scrapy.loader.processors import MapCompose


def get_required_skus(sku_jsonobject):
    if sku_jsonobject:
        return {
                "colour": sku_jsonobject.get("option0", 'None'),
                "price": sku_jsonobject.get("price_number", 'None'),
                "Currency": "Brazilian real",
                "size": sku_jsonobject.get("option1", 'None'),
                "previous_price": sku_jsonobject.get("compare_at_price_short", 'None'),
                "out_of_stock": not sku_jsonobject.get("available", 'None'),
                "sku_id": sku_jsonobject.get("sku", 'None')
        }


def get_gender_from_url(url):
    if 'Unisex' in url:
        return 'Unisex'
    if 'masculino' in url:
        return 'boy'

    return 'girl'


class ProductItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field(input_processor=MapCompose(lambda x: x.split(" ")[0]))
    price = scrapy.Field(input_processor=MapCompose(lambda x: float(x[2:].replace(',', '')) * 100))
    gender = scrapy.Field(input_processor=MapCompose(get_gender_from_url))
    skus = scrapy.Field(input_processor=MapCompose(get_required_skus), output_processor=lambda x: x)
    image_urls = scrapy.Field(input_processor=MapCompose(lambda x: f"http:{x}"),
                              output_processor=lambda x: x)
    description = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()),
                               output_processor=lambda x: ''.join(x))
