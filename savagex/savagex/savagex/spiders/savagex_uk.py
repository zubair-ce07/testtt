# -*- coding: utf-8 -*-

import json
import re

from scrapy import Spider, Request
from savagex.items import SavagexItem


class SavagexUkSpider(Spider):
    name = 'savagex.uk'
    start_urls = ['https://www.savagex.co.uk/']

    def parse(self, response):
        yield Request("https://www.savagex.co.uk/products", self.parse_first_page)

    def get_products(self, response):
        raw_json = re.findall(r'State\":\s*(.+),\s*\"initialP', response.text)
        if raw_json:
            json_data = raw_json[0]
            json_data = json.loads(json_data)
            return json_data
        else:
            None

    def parse_first_page(self, response):
        json_data = self.get_products(response)
        products = json_data["products"]["byMasterProductId"]
        for key, item in products.items():
            item_link = item["permalink"]+"-"+str(key)
            base_link = "https://www.savagex.co.uk/shop/"
            if not(item["color"]):
                base_link = base_link+"sets/"
            yield Request(url=base_link+item_link, callback=self.parse_item_details, dont_filter=True)

        next_page = "https://www.savagex.co.uk/api/products?aggs=false&includeOutOfStock=true&page=2&size=28&sort=newarrivals&excludeFpls=13511"
        header = {
            "x-api-key": "V0X9UnXkvO4vTk1gYHnpz7jQyAMO64Qp4ONV2ygu",
            "x-tfg-storedomain": "www.savagex.co.uk"
        }
        yield Request(url=next_page, callback=self.parse_pages, meta={"page": 2}, headers=header)

    def parse_pages(self, response):
        json_res = json.loads(response.text)
        for item in json_res:
            item_link = item["permalink"]+"-"+str(item["master_product_id"])
            base_link = "https://www.savagex.co.uk/shop/"
            if not(item["color"]):
                base_link = base_link+"sets/"
            yield Request(url=base_link+item_link, callback=self.parse_item_details, dont_filter=True)

        if json_res:
            page = response.meta.get("page")
            page = page + 1
            next_page = "https://www.savagex.co.uk/api/products?aggs=false&includeOutOfStock=true&page={}&size=28&sort=newarrivals&excludeFpls=13511".format(
                page)
            header = {
                "x-api-key": "V0X9UnXkvO4vTk1gYHnpz7jQyAMO64Qp4ONV2ygu",
                "x-tfg-storedomain": "www.savagex.co.uk"
            }
            yield Request(url=next_page, callback=self.parse_pages, meta={"page": page}, headers=header)

    def parse_item_details(self, response):
        json_data = self.get_products(response)
        item = list(json_data["products"]["byMasterProductId"].values())
        if item:
            item = item[0]
        else:
            return
        product = SavagexItem()
        product["name"] = item["label"]
        product["pid"] = item["item_number"].split("-")[0]
        product["description"] = [
            item["medium_description"], item["long_description"]]
        color = item["color"]
        link = "https://www.savagex.co.uk/shop/"
        if not(color):
            link = link + "sets/"
        product["url"] = link + item["permalink"] + \
            "-" + str(item["master_product_id"])
        product["images"] = []
        attributes = self.get_item_attributes(json_data)
        if attributes:
            product["attributes"] = attributes
        color_urls = [link+color_data["permalink"]+"-"+str(
            color_data["related_product_id"]) for color_data in item["related_product_id_object_list"]]
        first_color = color_urls[0]
        color_urls = color_urls[1:]
        if color:
            meta_dict = {
                "product": product,
                "color_urls": color_urls,
                "skus": {}
            }
            yield Request(url=first_color, callback=self.get_item_skus, meta=meta_dict, dont_filter=True)
        else:
            is_set = item.get("products_in_set")
            if is_set:
                currency = response.xpath(
                    "//meta[@property='og:price:currency']/@content").extract_first()
                yield from self.get_set_item_skus(product, item, currency)

    def get_item_attributes(self, json_data):
        item = list(json_data["products"]["byMasterProductId"].values())
        assets = json_data["assets"]["products_image_banner"]["assets"]
        attribute = {}
        if item:
            item = item[0]
            promo_ids = item["featured_product_location_id_list"]
            flag = True
            for promo_id in promo_ids:
                for asset in assets:
                    fpl_dict = dict(asset["options"]["customVars"])
                    fpl = fpl_dict.get("fpl")
                    if flag and (fpl == promo_id):
                        promo = asset["options"]["customVars"]["label"]
                        if "£" in promo:
                            attribute["promotion"] = asset["options"]["customVars"]["label"]
                            flag = False

        return attribute

    def get_set_item_skus(self, product, item, currency):
        item_sets = item["products_in_set"]
        skus = {}
        for one_set in item_sets:
            key = one_set["label"]+"_"+one_set["color"]
            available_sizes = [
                size["size"] for size in one_set["product_id_object_list"] if size["available_quantity"] > 0]
            price = item["retail_unit_price"]
            skus[key] = {
                "set": one_set["label"],
                "color": one_set["color"],
                "available_sizes": available_sizes,
                "price": price,
                "currency": currency,
            }
        product["skus"] = skus
        product["images"] = ["https:"+img for img in item["image_view_list"]]
        yield product

    def get_item_skus(self, response):
        json_data = self.get_products(response)
        if json_data:
            item = list(json_data["products"]["byMasterProductId"].values())
            skus = response.meta.get("skus")
            color_urls = response.meta.get("color_urls")
            product = response.meta.get("product")
            if item:
                item = item[0]
                currency = response.xpath(
                    "//meta[@property='og:price:currency']/@content").extract_first()
                color = item["color"]
                images = ["https:"+img for img in item["image_view_list"]]
                available = True if item["available_quantity_master"] > 0 else False
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
                next_color = color_urls[0]
                color_urls = color_urls[1:]
                meta_dict = {
                    "product": product,
                    "color_urls": color_urls,
                    "skus": skus,
                }
                yield Request(url=next_color, callback=self.get_item_skus, meta=meta_dict, dont_filter=True)
            else:
                product["skus"] = skus
                if skus == {}:
                    product["available"] = False
                else:
                    product["available"] = True
                yield product
