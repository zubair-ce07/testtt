# -*- coding: utf-8 -*-
import json
import re

from scrapy import Spider, Request
from savagex.items import SavagexItem


class SavagexCoSpider(Spider):
    name = 'savagex.co'
    start_urls = ['https://www.savagex.co.uk/']

    def parse(self, response):
        meta_dict = {
            "page": 1,
            "first_page": True,
        }
        yield Request("https://www.savagex.co.uk/products", self.parse_products, meta=meta_dict, dont_filter=True)

    def parse_products(self, response):
        page = response.meta.get("page")
        page = page + 1
        next_link = "https://www.savagex.co.uk/api/products?aggs=false&includeOutOfStock=true&page={}&size=28&sort=newarrivals&excludeFpls=13511".format(page)    
        meta_dict = {
            "page": page,
            "first_page": False
        }
        header = {
            "x-api-key": "V0X9UnXkvO4vTk1gYHnpz7jQyAMO64Qp4ONV2ygu",
        }
        first_page = response.meta.get("first_page")
        raw_json = re.findall(r'State\":\s*(.+),\s*\"initialP', response.text)
        if raw_json:
            json_data = json.loads(raw_json[0])
            products = json_data["products"]["byMasterProductId"]
            if first_page:
                for key, item in products.items():
                    item_link = item["permalink"]+"-"+str(key)
                    meta_dict = response.meta
                    meta_dict["first_page"] = False
                    yield Request("https://www.savagex.co.uk/shop/"+item_link, callback=self.parse_products, meta=meta_dict, dont_filter=True)
            else:
                yield from self.parse_item_details(json_data)
        else:
            products = json.loads(response.text)
            for item in products:
                item_link = item["permalink"]+"-"+str(item["master_product_id"])
                meta_dict = response.meta
                meta_dict["first_page"] = False
                yield Request("https://www.savagex.co.uk/shop/"+item_link, callback=self.parse_products, meta=meta_dict, dont_filter=True)
        
        yield Request(url=next_link, callback=self.parse_products, meta=meta_dict, headers=header)

    def parse_item_details(self, json_product):
        item_key = list(json_product["products"]["byMasterProductId"].keys())[0]
        item = json_product["products"]["byMasterProductId"][item_key]
        product = SavagexItem()
        product["name"] = item["label"]
        product["pid"] = item["item_number"].split("-")[0]
        product["description"] = [item["short_description"], item["medium_description"], item["long_description"]]
        color = item["color"]        
        link = "https://www.savagex.co.uk/shop/"
        if not(color):
            link  = link + "sets/"
        product["url"] = link + item["permalink"] + "-" + str(item["master_product_id"])
        color_urls = [link+color_data["permalink"]+"-"+str(color_data["related_product_id"]) for color_data in item["related_product_id_object_list"]]
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
            yield from self.get_clf_item_skus(json_product)
        
    def get_item_skus(self, response):
        skus = response.meta.get("skus")
        color_urls = response.meta.get("color_urls")
        product = response.meta.get("product")
        currency = response.xpath("//meta[@property='og:price:currency']/@content").extract_first()
        raw_json = re.findall(r'State\":\s*(.+),\s*\"initialP', response.text)
        if raw_json:
            json_data = json.loads(raw_json[0])
            item_key = list(json_data["products"]["byMasterProductId"].keys())[0]
            item = json_data["products"]["byMasterProductId"][item_key]
            color = item["color"]
            available_sizes = [size["size"] for size in item["product_id_object_list"] if size["available_quantity"] > 0]
            is_exclusive = [price["is_extra_exclusive"] for price in item["related_product_id_object_list"] if price["related_product_id"]==item["master_product_id"]][0]
            price = item["retail_unit_price"]
            if is_exclusive:
                price = item["default_unit_price"]

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
                yield Request(url=next_color, callback=self.get_item_skus, meta=meta_dict)
            else:
                product["skus"] = skus
                yield product

    def get_clf_item_skus(self, json_product):
        print("aya")
        pass

    def get_attributes(self, asset):
        pass
