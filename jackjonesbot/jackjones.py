# -*- coding: utf-8 -*-
import json
import re

import scrapy

from jackjonesbot.items import JackjonesProduct


class JackjonesSpider(scrapy.Spider):
    name = "jackjones"
    allowed_domains = ["jackjones.com.cn"]
    start_urls = ["https://www.jackjones.com.cn/api/service/init?channel=6"]

    token = ""
    category_urls_req = "https://www.jackjones.com.cn/assets/pc/JACKJONES/nav.json"
    category_url_t = "https://www.jackjones.com.cn/api/goods/{}&currentpage=1" \
                     "&sortDirection=desc&sortType=1"
    product_url_t = "https://www.jackjones.com.cn/detail/JACKJONES/{}.json"
    category_urls = []

    def parse(self, response):
        raw_token = json.loads(response.text)
        self.token = raw_token["data"]["token"]
        yield scrapy.Request(url=self.category_urls_req, callback=self.parse_category_urls)

    def parse_category_urls(self, response):
        raw_category_urls = json.loads(response.text)
        raw_category_urls = raw_category_urls["data"]
        self.process_category_urls(raw_category_urls)
        for category in self.category_urls:
            yield scrapy.Request(url=category, headers={"token": self.token},
                                 callback=self.parse_category)

    def process_category_urls(self, raw_urls):
        for raw_url in raw_urls:
            category_id = re.findall(r".*(goodsList\.html\?classifyIds=\d+).*",
                                     raw_url["navigationUrl"])

            if category_id:
                self.category_urls.append(self.category_url_t.format(
                    category_id[0].replace(".html", "")))

            sub_list = raw_url.get("list")

            if sub_list:
                self.process_category_urls(sub_list)
            else:
                continue

    def parse_category(self, response):
        raw_products = json.loads(response.text)
        total_pages = int(raw_products.get("totalPage"))
        current_page = int(raw_products.get("currentpage"))
        raw_products = raw_products.get("data")
        for raw_product in raw_products:
            yield scrapy.Request(url=self.product_url_t.format(raw_product["goodsCode"]),
                                 callback=self.parse_product)
        next_page = current_page + 1

        if next_page < total_pages:
            next_page_url = re.sub(r"currentpage=(\d+)", "currentpage=" +
                                   str(next_page), response.url)

            yield scrapy.Request(url=next_page_url, headers={"token": str(self.token)},
                                 callback=self.parse_category)

    def parse_product(self, response):
        product = JackjonesProduct()
        raw_product = json.loads(response.text)
        raw_product = raw_product["data"]
        product["product_id"] = self.product_id(raw_product)
        product["brand"] = "JACKJONES"
        product["care"] = self.product_care(raw_product)
        product["category"] = self.product_category(raw_product)
        product["description"] = self.product_description(raw_product)
        product["image_urls"] = self.image_urls(raw_product)
        product["name"] = self.product_name(raw_product)
        product["skus"] = self.skus(raw_product)
        product["url"] = response.url
        yield product

    def product_id(self, json_data):
        return json_data["projectCode"]

    def product_care(self, json_data):
        return json_data["goodsInfo"]

    def product_name(self, json_data):
        return json_data["goodsName"]

    def product_category(self, json_data):
        return json_data["color"][0]["categoryName"]

    def product_description(self, json_data):
        return json_data["describe"]

    def image_urls(self, raw_images):
        return [images.get("picurls") for images in raw_images.get("color")]

    def skus(self, raw_skus):
        skus = {}
        raw_colours = raw_skus["color"]
        for raw_colour in raw_colours:
            common_sku = self.product_pricing(raw_colour)
            raw_sizes = raw_colour["sizes"]
            for raw_size in raw_sizes:
                sku = common_sku.copy()
                sku["size"] = raw_size["size"]
                sku["colour"] = raw_colour["color"]

                if raw_colour["status"] != "InShelf":
                    sku["out_of_stock"] = True

                skus[sku["colour"] + "_" + sku["size"]] = sku
        return skus

    def product_pricing(self, raw_prices):
        prices = {"currency": "￥", "price": raw_prices["price"]}

        if prices["price"] != raw_prices["originalPrice"]:
            prices["previous_price"] = raw_prices["originalPrice"]
        return prices
