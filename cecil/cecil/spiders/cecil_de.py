# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request
from scrapy.selector import Selector
from cecil.items import CecilItem


class CecilDeSpider(Spider):
    name = 'cecil.de'
    start_urls = ['https://www.cecil.de/']
    header = {
        "x-shop": "3:de"
    }
    def parse(self, response):
        categories_link = "https://www.cecil.de/rest/web/category-tree-desktop"
        yield Request(categories_link, self.parse_categories, headers=self.header)
    
    def parse_categories(self, response):
        json_res = json.loads(response.text)
        for key in json_res:
            category = json_res[key]
            category_link = category["mainUrl"]
            if "Inspirations" not in category_link:
                yield Request("https://www.cecil.de/rest/web"+category_link, self.parse_item_links, headers=self.header)
        
    def parse_item_links(self, response):
        json_res = json.loads(response.text)
        for product_id in json_res["products"]:
            link = "https://www.cecil.de/rest/web/products?ids={}".format(product_id)
            yield Request(link, self.parse_product_detail, headers=self.header, dont_filter=True)
    
    def parse_product_detail(self, response):
        json_product = json.loads(response.text)
        json_product = json_product[0]
        product = CecilItem()
        product["url"] = "https://www.cecil.de"+json_product["mainUrl"]
        product["name"] = json_product["displayTitle"]
        product["pid"] = json_product["oxartnum"]
        product["available"] = True if json_product["stock"] > 0 else False
        product["description"] = self.get_item_description(json_product)
        product["attributes"] = self.get_item_attribute(json_product)
        breadcrum = json_product["seourl"]
        if breadcrum:
            breadcrum = breadcrum[0]["breadcrumb"]
            product["category"] = breadcrum[0]["title"]
            product["subcategory"] = [bread["title"] for bread in breadcrum[1:]]
        product["images"] = []
        colorVarients = [varient["oxid"] for varient in json_product["colorVariants"]]
        link = "https://www.cecil.de/rest/web/products?ids="+colorVarients[0]
        colorVarients = colorVarients[1:]
        meta_dict = {
            "product": product,
            "colorVarients" : colorVarients,
            "skus": {}
        }
        yield Request(link, self.get_item_skus, headers=self.header, meta=meta_dict, dont_filter=True)
    
    def get_item_description(self, product):
        raw_html_desc = product["longDesc"].strip()
        html_desc = Selector(text=raw_html_desc)
        description = html_desc.xpath("//text()").extract()
        description = [desc.strip() for desc in description if desc.strip()]
        return description

    def get_item_attribute(self, product):
        raw_html_desc = product["longDesc"].strip()
        html_desc = Selector(text=raw_html_desc)
        material = html_desc.xpath("//ul/li/text()").extract()[-1]
        return {
            "material": material
        }

    def get_item_skus(self, response):
        json_product = json.loads(response.text)
        json_product = json_product[0]
        product = response.meta.get("product")
        colorVarients = response.meta.get("colorVarients")
        skus = response.meta.get("skus")
        product["images"].extend(["https:"+json_product["pictures"][img] for img in json_product["pictures"]])
        price = json_product["discountedPrice"]
        was_price = json_product["price"]
        currency = "EUR"
        color = json_product["attributes"]["main_color"]
        sizes = [size["size"] for size in json_product["size"] if int(size["stock"])>0]
        if "" in sizes:
            sizes = [size["length"] for size in json_product["size"] if int(size["stock"])>0]
        skus[color] = {
            "color": color,
            "price": price,
            "available_sizes": sizes,
            "currency" : currency
        }
        if was_price > 0:
            skus[color]["was_price"] = was_price
        if colorVarients:
            link = "https://www.cecil.de/rest/web/products?ids="+colorVarients[0]
            colorVarients = colorVarients[1:]
            meta_dict = {
                "product": product,
                "colorVarients" : colorVarients,
                "skus": skus
            }
            yield Request(link, self.get_item_skus, headers=self.header, meta=meta_dict, dont_filter=True)
        else:
            product["skus"] = skus
            yield product
