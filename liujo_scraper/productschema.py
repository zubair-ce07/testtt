import json
import re
from parsel import Selector


def parse_category(selector):
    text = selector.css('script[type="text/javascript"]:contains("category")').extract_first()
    category = re.search(r'\'category\': "+(.+)"', text)
    return category.group(1).split("/") if category else []


def get_skus(selector):
    skus = {}
    price_selector = selector.css('.special-price>span[class=price]::text') or selector.css('.regular-price>span::text')
    old_prices = selector.css('.old-price>span[class=price]::text').extract_first()
    old_prices = re.findall(r"\d+\.\d+", old_prices) if old_prices else []
    common = {
        "colour": "one colour",
        "currency": re.search(r"\w{3}", price_selector.extract_first()).group(),
        "out_of_stock": False,
        "size": "one size",
        "price": float(re.search(r"\d+\.\d+", price_selector.extract_first()).group()),
        "previous-prices": [float(price) for price in old_prices],
        "sku_id": 'one colour_one size'
    }
    json_string = selector.css('script[type="application/ld+json"]::text').extract_first()
    if re.search(r'"@type": *"Product"', json_string):
        for raw_sku in json.loads(json_string):
            size = re.search(r"\w{16}([.\w\d]*)", raw_sku.get("mpn")).group(1)
            sku = common.copy()
            sku["colour"] = raw_sku.get("color")
            sku["out_of_stock"] = "InStock" not in raw_sku.get("offers").get("availability")
            sku["size"] = size if size != "T.U." else "one size"
            sku["sku_id"]: f'{raw_sku["colour"]}_{raw_sku["size"]}'
            skus[sku['sku_id']] = sku
    else:
        skus[common['sku_id']] = common
    return skus


def parse_product(response):
    selector = Selector(response.text)
    return {
        "name": selector.css('.product-name>h1::text').extract_first(),
        "gender": "girls",
        "description": selector.css('div[class="short-description-value"] ::text').extract(),
        "image_urls": selector.css(".slide>a>img::attr(data-more-views)").extract(),
        "care": [],
        "brand": selector.css('.branding>a::attr(title)').extract_first(),
        "url": response.url,
        "retailer_sku": selector.css('.product-ids::attr(data-sku)').extract_first()[:11],
        "category": parse_category(selector),
        "skus": get_skus(selector)
    }
