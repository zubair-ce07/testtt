import json
import re
from datetime import datetime

import requests

import scrapy
from lindex.items import LindexItem, LindexItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LindexSpider(CrawlSpider):
    name = "lindex"
    allowed_domains = ["www.lindex.com"]
    start_urls = ["http://www.lindex.com/uk/"]
    allow_re = ["/women/", "/lingerie/", "/beauty/", "/kids/"]
    deny_re = ["/sale/", "/new-in/", "guide", "giftcard"]

    rules = [Rule(LinkExtractor(allow=allow_re, deny=deny_re), callback="parse_list")]

    def find_data_page_count(self, response):
        if "total_pages" in response.meta:
            return response.meta["total_pages"]
        else:
            return int(response.css(".gridPages::attr(data-page-count)").extract_first())

    def find_current_page(self, response):
        if "page" in response.meta:
            return response.meta["page"]
        else:
            return 1

    def find_nodeId(self, response):
        if "nodeId" in response.meta:
            return response.meta["nodeId"]
        else:
            return response.css("body::attr(data-page-id)").extract_first()

    def find_product_id(self, response):
        return response.css(
            ".main_content .product_placeholder::attr(data-product-identifier)"
            ).extract_first()

    def find_product_urls(self, response):
        urls = response.css(".gridPage .img_wrapper > a::attr(href)").extract()
        return [response.urljoin(url) for url in urls]

    def find_colors(self, response):
        return response.css(".info_wrapper .colors a::attr(data-colorid)").extract()

    def parse_list(self, response):
        product_urls = self.find_product_urls(response)
        for url in product_urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

        node_id = self.find_nodeId(response)
        total_pages = self.find_data_page_count(response)
        curr_page = self.find_current_page(response)

        if curr_page < total_pages:
            yield scrapy.FormRequest(
                url="https://www.lindex.com/uk/SiteV3/Category/GetProductGridPage",
                headers={
                    "X-Requested-With": "XMLHttpRequest",
                    "Cache-Control": "no-cache",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Accept": "text/html, */*; q=0.01",
                    "Path": "/uk/SiteV3/Category/GetProductGridPage"
                },
                formdata={"nodeId": node_id, "pageIndex": str(curr_page)},
                meta={
                    "page": curr_page + 1,
                    "nodeId": node_id,
                    "total_pages": total_pages
                    },
                callback=self.parse_list
                )

    def develop_skus(self, response, content, item_loader):
        details = content["d"]
        loader = item_loader
        sizes = details["SizeInfo"]
        color_name = details["Color"]
        images = [image["Standard"] for image in details["Images"]]
        sku = []

        for i, size in enumerate(sizes):
            if i is not 0:
                size = re.split("[ -]", size["Text"])[0]
                sku.append({
                    "color": color_name,
                    "price": details["Price"],
                    "is_sold_out": details["IsSoldOut"],
                    "size": size,
                    "sku_id": "{}_{}".format(size, color_name)
                })
        loader.add_value("image_urls", images)
        loader.add_value("skus", sku)
        return loader

    def parse_product(self, response):
        loader = LindexItemLoader(item=LindexItem(), response=response)
        loader.add_css("uuid", ".main_content::attr(data-productid)")
        loader.add_css("retailer_sku", ".main_content .product_placeholder::attr(data-product-identifier)")
        loader.add_css("industry", ".main_content .product_placeholder::attr(data-style)")
        loader.add_css("name", ".name::text")
        loader.add_css("brand", ".main_content .product_placeholder::attr(data-product-brand)")
        loader.add_css("price", ".main_content .product_placeholder::attr(data-product-price)")
        loader.add_css("currency", ".totalPrice::text")
        loader.add_value("gender", "Women")
        loader.add_css("category", ".main_content .product_placeholder::attr(data-product-category)")
        loader.add_css("description", ".description ::text")
        loader.add_css("care", ".more_info ::text")
        loader.add_value("url_orignal", response.url)
        loader.add_css("url", "link[rel='canonical']::attr(href)")
        loader.add_value("date", datetime.now().strftime("%Y-%m-%d"))
        loader.add_css("market", ".selectedCountry[type='hidden']::attr(value)")
        loader.add_value("retailer", "lindex-uk")
        loader.add_value("spider_name", "lindex-uk-crawl")
        loader.add_value("crawl_id", f"lindex-uk-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj")
        loader.add_value("crawl_start_time", datetime.now().isoformat())

        colors = self.find_colors(response)
        for color in colors:
            new_response = requests.post(
                url="https://www.lindex.com/WebServices/ProductService.asmx/GetProductData",
                headers={
                        "X-Requested-With": "XMLHttpRequest",
                        "Cache-Control": "no-cache",
                        "Content-Type": "application/json; charset=UTF-8",
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                    },
                json={
                    "productIdentifier": self.find_product_id(response),
                    "colorId": color,
                    "primaryImageType": "1"
                    }
                )
            self.develop_skus(new_response, json.loads(new_response.content), loader)
        yield loader.load_item()
