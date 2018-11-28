import json
import re

import scrapy

from savagexbot.items import SavagexProduct


class SavagexSpider(scrapy.Spider):
    name = "savagex"
    allowed_domains = ["savagex.co.uk"]
    start_urls = ["http://www.savagex.co.uk"]

    api_key = ""

    category_url_t = "https://www.savagex.co.uk/api/products?aggs=false&includeOutOfStock=true" \
                     "&page=1&size=1000&{}={}&sort=newarrivals&excludeFpls=13511"
    product_url_t = "https://www.savagex.co.uk/shop/{}-{}"

    def parse(self, response):
        css = "#__next-error + script::text"
        raw_categories = response.css(css).extract_first().replace("__CONFIG__ = ", "")
        raw_categories = json.loads(raw_categories)
        self.api_key = raw_categories["api"]["key"]
        raw_categories = raw_categories["productBrowser"]["sections"]
        category_ids = re.findall(r"(defaultProductCategoryIds)\': (\d+)", str(raw_categories))
        for cate_type, cate_id in category_ids:
            yield scrapy.Request(
                url=self.category_url_t.format(cate_type, cate_id.strip()),
                callback=self.parse_category,
                headers={"x-api-key": self.api_key, "x-tfg-storedomain": "www.savagex.co.uk"})

    def parse_category(self, response):
        if response.text:
            raw_category_page = json.loads(response.text)
            for raw_product in raw_category_page:
                yield scrapy.Request(
                    url=self.product_url_t.format(
                        raw_product["permalink"].lower(),
                        raw_product["master_product_id"]), callback=self.parse_product)

            current_page = int(re.findall(r"page=(\d+)", response.url)[0])
            next_page = re.sub(r"page=(\d+)", "page=" + str(current_page + 1), response.url)
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_category,
                headers={"x-api-key": self.api_key, "x-tfg-storedomain": "www.savagex.co.uk"})

    def parse_product(self, response):
        css = "script:nth-child(5)::text"
        raw_product = response.css(css).re_first(r"({\"props.*),\"pathname.*")
        raw_product = re.sub(r"\"\\\"|\\\"\"", "\"", raw_product).replace("\\\"", "'")
        raw_product = raw_product.replace("\xa0", "") + "}"
        raw_product = json.loads(raw_product)["props"]["initialProps"]["product"]
        product = SavagexProduct()
        product["product_id"] = self.product_id(raw_product)
        product["brand"] = "Savage X"
        product["name"] = self.product_name(raw_product)
        product["care"] = self.product_care(raw_product)
        product["description"] = self.product_description(raw_product) or []
        product["url"] = response.url
        product["image_urls"] = self.image_urls(raw_product)
        product["skus"] = self.skus(raw_product)
        yield product

    def product_id(self, raw_product):
        return raw_product["master_product_id"]

    def product_name(self, raw_product):
        return raw_product["label"]

    def product_care(self, raw_product):
        return raw_product.get("medium_description", "").split("\n")

    def product_description(self, raw_product):
        if raw_product.get("long_description"):
            return raw_product.get("long_description", "").split(",")

    def image_urls(self, raw_product):
        return raw_product["image_view_list"]

    def skus(self, raw_product):
        raw_skus = raw_product["related_product_id_object_list"]
        price = self.product_pricing(raw_product)
        skus = {}
        for raw_colour in raw_skus:
            colour = raw_colour["color"]
            for raw_size in raw_colour["product_id_object_list"]:
                size = raw_size["size"]
                sku = {"colour": colour, "currency": "EUR", "price": price, "size": size}

                if False if raw_size["availability"] == "in stock" else True:
                    sku["out_of_stock"] = True

                skus[f"{colour}_{size}"] = sku
        return skus

    def product_pricing(self, raw_product):
        return raw_product["retail_unit_price"]
