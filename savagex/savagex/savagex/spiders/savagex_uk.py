# -*- coding: utf-8 -*-

import json
import re

from scrapy import Spider, Request
from savagex.items import SavagexItem


class SavagexUkSpider(Spider):
    name = 'savagex.uk'
    start_urls = ['https://www.savagex.co.uk/products']
    header = {
        "x-api-key": "V0X9UnXkvO4vTk1gYHnpz7jQyAMO64Qp4ONV2ygu",
        "x-tfg-storedomain": "www.savagex.co.uk"
    }

    def parse(self, response):
        raw_product = self.get_products(response)
        products = raw_product["products"]["byMasterProductId"]

        for key, item in products.items():
            base_link = "https://www.savagex.co.uk/shop/"

            if not item["color"]:
                base_link = "{}{}".format(base_link, "sets/")

            item_link = "{}{}-{}".format(base_link,
                                         item["permalink"], item["master_product_id"])

            yield Request(url=item_link, callback=self.parse_item_details, dont_filter=True)

        next_page_url = "https://www.savagex.co.uk/api/products?" \
            "aggs=false&includeOutOfStock=true&page=2&size=28&sort=newarrivals&excludeFpls=13511"
        yield Request(url=next_page_url, callback=self.parse_pages, meta={"page_num": 2}, headers=self.header)

    def get_products(self, response):
        raw_product = re.findall(
            r'State\":\s*(.+),\s*\"initialP', response.text)

        if raw_product:
            return json.loads(raw_product[0])

    def parse_pages(self, response):
        products = json.loads(response.text)

        for item in products:
            base_link = "https://www.savagex.co.uk/shop/"

            if not item["color"]:
                base_link = "{}{}".format(base_link, "sets/")

            item_link = "{}{}-{}".format(base_link,
                                         item["permalink"], item["master_product_id"])
            yield Request(url=item_link, callback=self.parse_item_details, dont_filter=True)

        if products:
            page_num = response.meta.get("page_num")
            page_num = page_num + 1
            next_page_url = "https://www.savagex.co.uk/api/products?"\
                "aggs=false&includeOutOfStock=true&page={}&size=28&sort=newarrivals&excludeFpls=13511".format(
                    page_num)
            yield Request(url=next_page_url, callback=self.parse_pages, meta={"page_num": page_num}, headers=self.header)

    def parse_item_details(self, response):
        raw_product = self.get_products(response)
        item = list(raw_product["products"]["byMasterProductId"].values())

        if not item:
            return

        item = item[0]
        product = SavagexItem()
        product["name"] = item["label"]
        product["pid"] = item["item_number"].split("-")[0]
        product["description"] = [
            item["medium_description"], item["long_description"]]
        color = item["color"]
        link = "https://www.savagex.co.uk/shop/"

        if not color:
            link = "{}{}".format(link, "sets/")

        product["url"] = "{}{}-{}".format(link,
                                          item["permalink"], item["master_product_id"])
        product["images"] = []
        attributes = self.get_item_attributes(raw_product)

        if attributes:
            product["attributes"] = attributes

        color_urls = ["{}{}-{}".format(link, color_data["permalink"], color_data["related_product_id"])
                      for color_data in item["related_product_id_object_list"]]
        first_color = color_urls[0]
        color_urls = color_urls[1:]

        if color:
            meta = {
                "product": product,
                "color_urls": color_urls,
                "skus": {}
            }
            yield Request(url=first_color, callback=self.get_item_skus, meta=meta, dont_filter=True)
        elif "products_in_set" in item:
            currency = response.xpath(
                "//meta[@property='og:price:currency']/@content").extract_first()
            yield from self.get_set_item_skus(product, item, currency)

    def get_item_attributes(self, raw_product):
        item = list(raw_product["products"]["byMasterProductId"].values())
        assets = raw_product["assets"]["products_image_banner"]["assets"]
        attribute = {}

        if not item:
            return attribute

        item = item[0]
        promo_ids = item["featured_product_location_id_list"]
        flag = True

        for promo_id in promo_ids:

            for asset in assets:
                fpl_dict = dict(asset["options"]["customVars"])
                fpl = fpl_dict.get("fpl")

                if flag and fpl == promo_id:
                    promo = asset["options"]["customVars"]["label"]

                    if "£" not in promo:
                        continue
                    attribute["promotion"] = asset["options"]["customVars"]["label"]
                    flag = False

        return attribute

    def get_set_item_skus(self, product, item, currency):
        item_sets = item["products_in_set"]
        skus = {}

        for one_set in item_sets:
            key = "{}_{}".format(one_set["label"], one_set["color"])
            available_sizes = [
                size["size"] for size in one_set["product_id_object_list"] if size["available_quantity"]]
            price = item["retail_unit_price"]
            skus[key] = {
                "set": one_set["label"],
                "color": one_set["color"],
                "available_sizes": available_sizes,
                "price": price,
                "currency": currency,
            }

        product["skus"] = skus
        product["images"] = ["https:{}".format(img) for img in item["image_view_list"]]
        return dict(product)

    def get_item_skus(self, response):
        raw_product = self.get_products(response)

        if not raw_product:
            return

        item = list(raw_product["products"]["byMasterProductId"].values())
        skus = response.meta.get("skus")
        color_urls = response.meta.get("color_urls")
        product = response.meta.get("product")

        if not item:
            return

        item = item[0]
        currency = response.xpath(
            "//meta[@property='og:price:currency']/@content").extract_first()
        color = item["color"]
        images = ["https:{}".format(img) for img in item["image_view_list"]]
        available = item["available_quantity_master"] > 0
        available_sizes = [
            size["size"] for size in item["product_id_object_list"] if size["available_quantity"] > 0]
        is_exclusive = [price["is_extra_exclusive"] for price in item["related_product_id_object_list"]
                        if price["related_product_id"] == item["master_product_id"]][0]
        price = item["retail_unit_price"]

        if is_exclusive:
            price = item["default_unit_price"]

        product["images"].extend(images)

        if available:
            skus[color] = {
                "color": color,
                "available_sizes": available_sizes,
                "price": price,
                "currency": currency,
            }

        if color_urls:
            next_color_url = color_urls[0]
            color_urls = color_urls[1:]
            meta = {
                "product": product,
                "color_urls": color_urls,
                "skus": skus,
            }
            return Request(url=next_color_url, callback=self.get_item_skus, meta=meta, dont_filter=True)
        else:
            product["skus"] = skus
            product["available"] = bool(skus)
            return dict(product)
