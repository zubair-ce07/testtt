# -*- coding: utf-8 -*-

import json
import re

from scrapy import Spider, Request

from savagex.items import SavagexItem


class SavagexUkSpider(Spider):
    name = 'savagex.uk'
    start_urls = ['https://www.savagex.co.uk/products']
    base_item_link = "https://www.savagex.co.uk/shop/"
    headers = {
        "x-api-key": "V0X9UnXkvO4vTk1gYHnpz7jQyAMO64Qp4ONV2ygu",
        "x-tfg-storedomain": "www.savagex.co.uk"
    }

    custom_settings = {
        "ITEM_PIPELINES": {
            "savagex.pipelines.FilterDuplicate": 300,
        },
        "ROBOTSTXT_OBEY": False,
    }

    def parse(self, response):
        raw_product = self.get_products(response)
        products = raw_product["products"]["byMasterProductId"]

        for key, item in products.items():
            base_link = self.base_item_link

            if not item["color"]:
                base_link = "{}sets/".format(base_link)

            item_link = "{}{}-{}".format(base_link,
                                         item["permalink"], item["master_product_id"])

            yield Request(url=item_link, callback=self.parse_item_details, dont_filter=True)

        next_page_url = "https://www.savagex.co.uk/api/products?" \
            "aggs=false&includeOutOfStock=true&page=2&size=28&sort=newarrivals&excludeFpls=13511"
        yield Request(url=next_page_url, callback=self.parse_pages,\
                meta={"page_num": 2}, headers=self.headers)

    def get_products(self, response):
        raw_product = re.findall(
            r'State\":\s*(.+),\s*\"initialP', response.text)

        if raw_product:
            return json.loads(raw_product[0])

    def parse_pages(self, response):
        products = json.loads(response.text)

        for item in products:
            base_link = self.base_item_link

            if not item["color"]:
                base_link = "{}sets/".format(base_link)

            item_link = "{}{}-{}".format(base_link,
                                         item["permalink"], item["master_product_id"])
            yield Request(url=item_link, callback=self.parse_item_details, dont_filter=True)

        if products:
            page_num = response.meta["page_num"]
            page_num = page_num + 1
            next_page_url = "https://www.savagex.co.uk/api/products?aggs=false&"\
                "includeOutOfStock=true&page={}&size=28&sort=newarrivals&"\
                "excludeFpls=13511".format(page_num)
            yield Request(url=next_page_url, callback=self.parse_pages,
                          meta={"page_num": page_num}, headers=self.headers)

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
        base_link = self.base_item_link

        if not color:
            base_link = "{}sets/".format(base_link)

        product["url"] = "{}{}-{}".format(base_link,
                                          item["permalink"], item["master_product_id"])
        product["images"] = []
        attributes = self.get_item_attributes(raw_product)

        if attributes:
            product["attributes"] = attributes

        color_urls = ["{}{}-{}".format(base_link, color_data["permalink"], color_data["related_product_id"])
                      for color_data in item["related_product_id_object_list"]]
        first_color_url = color_urls.pop()

        if color:
            meta = {
                "product": product,
                "color_urls": color_urls,
                "skus": {}
            }
            return Request(url=first_color_url, callback=self.get_item_skus, meta=meta, dont_filter=True)
        elif "products_in_set" in item:
            currency = response.xpath(
                "//meta[@property='og:price:currency']/@content").extract_first()
            return self.get_set_item_skus(product, item, currency)

    def get_item_attributes(self, raw_product):
        item = list(raw_product["products"]["byMasterProductId"].values())
        assets = raw_product["assets"].get("products_image_banner")
        attribute = {}

        if not item or not assets:
            return attribute
        assets = assets["assets"]
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
            available_sizes = [size["size"] for size in one_set["product_id_object_list"]
                               if size["available_quantity"]]
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
        available = bool(item["available_quantity_master"])
        available_sizes = [
            size["size"] for size in item["product_id_object_list"] if size["available_quantity"]]
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
            next_color_url = color_urls.pop()
            meta = {
                "product": product,
                "color_urls": color_urls,
                "skus": skus,
            }
            return Request(url=next_color_url, callback=self.get_item_skus,\
                        meta=meta, dont_filter=True)
        else:
            product["skus"] = skus
            product["available"] = bool(skus)
            return dict(product)
