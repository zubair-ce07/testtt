# -*- coding: utf-8 -*-
import re
import json
import scrapy
from jackjonesbot.items import JackjonesProduct


class JackjonesSpider(scrapy.Spider):
    name = 'jackjones'
    allowed_domains = ['jackjones.com.cn']
    start_urls = ['https://www.jackjones.com.cn/assets/pc/JACKJONES/nav.json']
    token = "eyJqdGkiOiI4Ulg2dDViRHlHIiwiaWF0IjoxNTM5MjUzMzc1LCJjaGFubmVsI" \
        + "joiNiJ9.WznZGroP1OD5EI8E6UR5mvEOr2K_nTnKgNuGYNQq7H8"

    def parse(self, response):
        category_urls = self.get_all_category_urls(response)

        processed_cate_urls = self.process_category_url(category_urls)

        for category in processed_cate_urls:
            yield scrapy.Request(
                url=category,
                headers={"token": str(self.token)},
                callback=self.parse_products
            )

    def get_all_category_urls(self, response):
        category_links = []
        json_data = json.loads(response.text)
        super_nodes = json_data["data"]

        for super_node in super_nodes:
            if bool(
                    re.search(r'.*goodsList.*', super_node["navigationUrl"])
            ):
                category_links.append(super_node["navigationUrl"])
            parent_nodes = super_node["list"]
            for parent_node in parent_nodes:
                if bool(
                        re.search(r'.*goodsList.*',
                                  parent_node["navigationUrl"])
                ):
                    category_links.append(parent_node["navigationUrl"])
                sub_nodes = parent_node["list"]
                for sub_node in sub_nodes:
                    if bool(
                            re.search(r'.*goodsList.*',
                                      sub_node["navigationUrl"])
                    ):
                        category_links.append(sub_node["navigationUrl"])

        return category_links

    def get_token(self, response):
        json_data = json.loads(response.text)
        self.token = json_data["data"]["token"]

    def process_category_url(self, categorise):
        category_ids = [
            re.search(
                r'.*(goodsList\.html\?classifyIds=\d+)', i
            ).group(1) for i in categorise
        ]
        category_start_url = "https://www.jackjones.com.cn/api/goods/"
        category_end_url = "&currentpage=1&sortDirection=desc&sortType=1"

        urls = [
            category_start_url + i + category_end_url for i in category_ids
        ]

        urls = [i.replace(".html", "") for i in urls]

        urls = list(set(urls))

        return urls

    def parse_products(self, response):
        json_data = json.loads(response.text)
        total_pages = int(json_data["totalPage"])
        current_page = int(json_data["currentpage"])

        prodcuts = json_data["data"]

        for prodcut in prodcuts:
            prodcut_code = prodcut["goodsCode"]
            prodcut_start_url = "https://www.jackjones.com.cn/detail/JACKJONES"
            prodcut_url = prodcut_start_url + "/" + prodcut_code + ".json"

            yield scrapy.Request(
                url=prodcut_url,
                callback=self.parse_product_details
            )

        next_page = current_page + 1
        if next_page < total_pages:
            next_page_url = re.sub(
                r'currentpage=(\d+)', "currentpage=" +
                str(next_page), response.url
            )
            yield scrapy.Request(
                url=next_page_url,
                headers={"token": str(self.token)},
                callback=self.parse_products
            )

    def parse_product_details(self, response):
        product = JackjonesProduct()
        json_data = json.loads(response.text)
        json_data = json_data["data"]

        product["product_id"] = json_data["projectCode"]
        product["brand"] = 'JACKJONES'
        product["care"] = json_data["goodsInfo"]
        product["category"] = json_data["color"][0]["categoryName"]
        product["description"] = json_data["describe"]
        product["image_urls"] = self.get_img_urls(json_data)
        product["name"] = json_data["goodsName"]
        product["skus"] = self.get_skus_detail(json_data)
        product["url"] = response.url

        yield product

    def get_img_urls(self, json_data):
        img_urls = []
        img_nodes = json_data["color"]
        for node in img_nodes:
            img_urls.append(node["picurls"])

        return img_urls

    def get_skus_detail(self, json_data):
        skus = {}
        colour_nodes = json_data["color"]

        for colour_node in colour_nodes:
            colour = colour_node["color"]
            previouse_price = colour_node["originalPrice"]
            price = colour_node["price"]
            size_nodes = colour_node["sizes"]

            for size_node in size_nodes:
                size = size_node["size"]
                skus[colour + '_' + size] = {
                    "colour": colour,
                    "currency": "",
                    "previouse_price": previouse_price,
                    "price": price,
                    "size": size,
                }

        return skus
