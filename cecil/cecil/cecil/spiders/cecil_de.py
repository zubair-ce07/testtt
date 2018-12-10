# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request
from scrapy.selector import Selector

from cecil.items import CecilItem


class CecilDeSpider(Spider):
    name = "cecil.de"
    headers = {
        "x-shop": "3:de"
    }

    custom_settings = {
        "ITEM_PIPELINES": {
            "cecil.pipelines.FilterDuplicate": 300,
        },
        "ROBOTSTXT_OBEY": False,
    }

    def start_requests(self):
        categories_link = "https://www.cecil.de/rest/web/category-tree-desktop"
        yield Request(categories_link, self.parse_categories, headers=self.headers)

    def parse_categories(self, response):
        products = json.loads(response.text)

        for category in products.values():
            category_link = category["mainUrl"]

            if "Inspirations" in category_link:
                continue
            yield Request("https://www.cecil.de/rest/web{}".format(category_link),
                              self.parse_product_links, headers=self.headers)

    def parse_product_links(self, response):
        products = self.get_product(response)

        if not products:
            return

        for product_id in products["products"]:
            link = "https://www.cecil.de/rest/web/products?ids={}".format(
                product_id)
            yield Request(link, self.parse_product_detail, headers=self.headers, dont_filter=True)

    def parse_product_detail(self, response):
        raw_product = self.get_product(response)

        if not raw_product:
            return

        raw_product = raw_product[0]
        product = CecilItem()
        product["url"] = "https://www.cecil.de{}".format(
            raw_product["mainUrl"])
        product["name"] = raw_product["displayTitle"]
        product["pid"] = raw_product["oxartnum"]
        product["available"] = bool(raw_product["stock"])
        product["description"] = self.get_item_description(raw_product)
        product["attributes"] = self.get_item_attribute(raw_product)
        breadcrumbs = raw_product["seourl"]

        if breadcrumbs:
            breadcrumbs = breadcrumbs[0]["breadcrumb"]
            product["category"] = breadcrumbs[0]["title"]
            product["subcategory"] = [breadcrum["title"]
                                      for breadcrum in breadcrumbs[1:]]
        product["images"] = []
        color_urls = ["https://www.cecil.de/rest/web/products?ids={}".format(varient["oxid"])
                      for varient in raw_product["colorVariants"]]
        color_link = color_urls.pop()
        meta = {
            "product": product,
            "color_urls": color_urls,
            "skus": {}
        }
        yield Request(color_link, self.get_item_skus, headers=self.headers, meta=meta, dont_filter=True)

    def get_product(self, response):
        return json.loads(response.text.replace('motion":,', 'motion":{},'))

    def get_item_description(self, product):
        desc = Selector(text=product["longDesc"].strip())
        description = desc.xpath("//text()").extract()
        description = [desc.strip() for desc in description if desc.strip()]
        return description

    def get_item_attribute(self, product):
        attrib = Selector(text=product["longDesc"].strip())
        material = attrib.xpath("//ul/li/text()").extract()[-1]
        return {"material": material}

    def get_item_skus(self, response):
        raw_product = self.get_product(response)

        if not raw_product:
            return

        raw_product = raw_product[0]
        product = response.meta.get("product")
        color_urls = response.meta.get("color_urls")
        skus = response.meta.get("skus")
        product["images"].extend(
            ["https:{}".format(raw_product["pictures"][img]) for img in raw_product["pictures"]])
        price = raw_product["discountedPrice"]
        was_price = raw_product["price"]
        currency = "EUR"
        color = raw_product["attributes"]["main_color"]
        sizes = [size["size"]
                 for size in raw_product["size"] if int(size["stock"])]

        if "" in sizes:
            sizes = [size["length"]
                     for size in raw_product["size"] if int(size["stock"])]

        skus[color] = {
            "color": color,
            "price": price,
            "available_sizes": sizes,
            "currency": currency
        }

        if was_price:
            skus[color]["was_price"] = was_price

        if color_urls:
            next_color_link = color_urls.pop()
            meta = {
                "product": product,
                "color_urls": color_urls,
                "skus": skus
            }
            return Request(next_color_link, self.get_item_skus, \
                        headers=self.headers, meta=meta, dont_filter=True)
        else:
            product["skus"] = skus
            return dict(product)
