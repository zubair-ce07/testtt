import json
import re

import scrapy

from jackjonesbot.items import JackjonesProduct


class JackjonesSpider(scrapy.Spider):
    name = "jackjones"
    allowed_domains = ["jackjones.com.cn"]
    start_urls = ["https://www.jackjones.com.cn/api/service/init?channel=6"]

    headers = ""
    category_req_url = "https://www.jackjones.com.cn/assets/pc/JACKJONES/nav.json"
    category_url_t = "https://www.jackjones.com.cn/api/goods/goodsList?classifyIds" \
                     "={}&currentpage=1&sortDirection=desc&sortType=1"
    product_url_t = "https://www.jackjones.com.cn/detail/JACKJONES/{}.json"

    def parse(self, response):
        raw_headers = json.loads(response.text)
        self.headers = raw_headers["data"]["token"]
        yield scrapy.Request(url=self.category_req_url, callback=self.parse_category_urls)

    def parse_category_urls(self, response):
        category_urls = self.process_category_urls(response.text)
        for category in category_urls:
            yield scrapy.Request(url=category, headers={"token": self.headers},
                                 callback=self.parse_category)

    def process_category_urls(self, raw_urls):
        return [self.category_url_t.format(category_id) for category_id in
                re.findall(r"\"navigationUrl\":\"\D*(\d+)\"", raw_urls)]

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

            yield scrapy.Request(url=next_page_url, headers={"token": str(self.headers)},
                                 callback=self.parse_category)

    def parse_product(self, response):
        product = JackjonesProduct()
        raw_product = json.loads(response.text)["data"]
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

    def product_id(self, raw_product):
        return raw_product["projectCode"]

    def product_care(self, raw_product):
        return raw_product["goodsInfo"]

    def product_name(self, raw_product):
        return raw_product["goodsName"]

    def product_category(self, raw_product):
        return raw_product["color"][0]["categoryName"]

    def product_description(self, raw_product):
        return raw_product["describe"]

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

                skus[f"{sku['colour']}_{sku['size']}"] = sku
        return skus

    def product_pricing(self, raw_prices):
        prices = {"currency": "￥", "price": raw_prices["price"]}

        if prices["price"] != raw_prices["originalPrice"]:
            prices["previous_price"] = raw_prices["originalPrice"]
        return prices
