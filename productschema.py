import json
import re
from parsel import Selector


def parse_price(selector):
    return re.search( r"\d+\.\d+",
                      selector.css('.special-price>span[class=price]::text').extract_first() or selector.css(
                            '.regular-price>span::text').extract_first()).group()


def previous_prices(selector):
    old_price = selector.css('.old-price>span[class=price]::text').extract_first()
    return [re.search(r"\d+\.\d+", old_price).group()] if old_price else []


def parse_description(selector):
    description = selector.css('div[class="short-description-value"] ::text').extract()
    return re.sub(r"[\r\n]+", " ", ''.join(description).strip()).split(". ")


def parse_category(selector):
    for text in selector.css('script[type="text/javascript"]::text').extract():
        if "category" in text:
            return re.search(r'\'category\': "+(.+)"', text).group(1).split("/")


def single_product(selector):
    return {
        "colour":          "one colour",
        "currency":        re.search(r"\w{3}", selector.css('.price::text').extract_first()).group(),
        "out_of_stock":    False,
        "size":            "one size",
        "price":           parse_price(selector),
        "previous-prices": previous_prices(selector),
        "sku_id":          'one colour_one size'
    }


def yield_sku(selector):
    json_string = selector.css('script[type="application/ld+json"]::text').extract_first()
    if re.search(r'"@type": *"Product"', json_string):
        price = parse_price(selector),
        previous = previous_prices(selector),
        for raw_sku in json.loads(json_string):
            size = re.search(r"\w{16}([.\w\d]*)", raw_sku.get("mpn")).group(1)
            yield {
                "colour":          raw_sku.get("color"),
                "currency":        raw_sku.get("offers").get("priceCurrency"),
                "out_of_stock":    "InStock" not in raw_sku.get("offers").get("availability"),
                "size":            size if size != "T.U." else "one size",
                "price":           price,
                "previous-prices": previous,
                "sku_id":          f'{raw_sku.get("color")}_{size}'
            }
    else:
        yield single_product(selector)


def parse_product(response):
    selector = Selector(response.text)
    return {
        "name":         selector.css('.product-name>h1::text').extract_first(),
        "gender":       "girls",
        "description":  parse_description(selector),
        "image_urls":   selector.css(".slide>a>img::attr(data-more-views)").extract(),
        "care":         [],
        "brand":        selector.css('.branding>a::attr(title)').extract_first(),
        "url":          response.url,
        "retailer_sku": selector.css('.product-ids::attr(data-sku)').extract_first()[:11],
        "category":     parse_category(selector),
        "skus":         {sku.get("sku_id"): sku for sku in yield_sku(selector)}
    }
