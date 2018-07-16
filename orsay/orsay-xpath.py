import json
from copy import deepcopy

import requests
from parsel import Selector


def xpath_parser(response):
    item = Item()
    item.processed_by = "xpath"
    item.url = response.url
    response = Selector(response.text)
    item.brand = "Orsay"
    item.name = response.xpath("//h1[@class='product-name']/text()").extract_first()
    item.description = response.xpath("//div[@class='with-gutter']/text()").extract()
    item.care = response.xpath("//div[contains(@class,'product-material')]/p/text()").extract()
    item.image_urls = response.xpath("//img[@class='productthumbnail']/@src").extract()
    product_description = response.xpath("//div[@class='js-product-content-gtm']/@data-product-details").extract_first()
    product_description = json.loads(product_description)
    item.retailer_sku = product_description["productId"]
    color_urls = response.xpath("//a[contains(@class,'js-color-swatch')]/@href").extract()
    items = []
    for color_url in color_urls:
        items.append(parse_color(deepcopy(item), color_url))
    return items


def parse_color(item, color_url):
    response = requests.get(color_url)
    response = Selector(response.text)
    size_list = response.xpath("//a[contains(@class,'swatchanchor js-color-link')]/text()").extract()
    color = response.xpath("//span[@class='selected-value']/text()").extract_first()
    price = response.xpath("//span[@class='price-sales']/text()").extract_first()
    for size in size_list:
        item.skus.update({
            "{}_{}".format(item.retailer_sku, size.strip("\n")): {
                "color": color,
                "size": size.strip("\n"),
                "price": price.strip("\n")
            }
        })
    return item


def css_parser(response):
    item = Item()
    item.processed_by = "CSS"
    item.url = response.url
    response = Selector(response.text)
    item.name = response.css("h1.product-name::text").extract_first()
    item.description = response.css(".with-gutter::text").extract()
    item.image_urls = response.css(".productthumbnail::attr(src)").extract()
    item.care = response.css("div.product-info-title + p::text").extract()
    item.brand = "Orsay"
    product_description = response.css(".js-product-content-gtm::attr(data-product-details)").extract_first()
    product_description = json.loads(product_description)
    item.retailer_sku = product_description["productId"]
    return item


class Item:
    processed_by = ""
    brand = ""
    care = []
    description = []
    image_urls = []
    name = ""
    retailer_sku = ""
    skus = {}
    url = ""

    def __str__(self):
        for key, value in self.__dict__.items():
            print(key.upper())
            print(value)
        return "\n"


if __name__ == "__main__":
    item_response = requests.get("http://www.orsay.com/de-de/elegantes-kleid-in-wickel-optik-470127526000.html")
    if item_response.status_code == requests.codes.ok:
        print(css_parser(item_response))
        [print(item) for item in xpath_parser(item_response)]
