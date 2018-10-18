import json
import re
from datetime import datetime

import scrapy
from lindex.items import LindexItem, LindexItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LindexSpider(CrawlSpider):
    name = "lindex"
    allowed_domains = ["www.lindex.com"]
    start_urls = ["http://www.lindex.com/uk/"]
    listing_css = [".mega_menu_box"]
    products_css = [".gridPage .img_wrapper"]
    deny_re = [
        "/sale/", "/new-in/",
        "guide", "giftcard",
        "/children-wear/", "/campaign/", "/Assets/"
        ]
    rules = [
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_re), callback="parse_list"),
        Rule(LinkExtractor(restrict_css=products_css, deny=deny_re), callback="parse_product")
    ]

    def extract_pages_count(self, response):
        if "total_pages" in response.meta:
            return response.meta["total_pages"]
        else:
            return int(response.css(
                ".gridPages::attr(data-page-count)").extract_first())

    def extract_current_page(self, response):
        if "page" in response.meta:
            return response.meta["page"]
        else:
            return 1

    def extract_nodeId(self, response):
        if "nodeId" in response.meta:
            return response.meta["nodeId"]
        else:
            return response.css("body::attr(data-page-id)").extract_first()

    def extract_product_id(self, response):
        return response.css(
            ".main_content .product_placeholder::attr(data-product-identifier)"
            ).extract_first()

    def extract_colors(self, response):
        return response.css(
            ".info_wrapper .colors a::attr(data-colorid)").extract()

    def parse_list(self, response):
        node_id = self.extract_nodeId(response)
        total_pages = self.extract_pages_count(response)
        curr_page = self.extract_current_page(response)

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
                callback=self.parse
                )

    def has_more_colors(self, response, colors, loader):
        if len(colors) == 0:
            yield loader.load_item()
        else:
            yield scrapy.Request(
                url="https://www.lindex.com/WebServices/ProductService.asmx/GetProductData",
                headers={
                        "X-Requested-With": "XMLHttpRequest",
                        "Content-Type": "application/json; charset=UTF-8",
                    },
                method="POST",
                body=json.dumps({
                    "productIdentifier": self.extract_product_id(response),
                    "colorId": colors.pop(0),
                    "primaryImageType": "1"
                    }),
                meta={"loader": loader, "colors": colors},
                callback=self.skus
            )

    def skus(self, response):
        details = json.loads(response.body)["d"]
        loader = response.meta["loader"]
        sizes = details["SizeInfo"]
        color_name = details["Color"]
        images = [image["Standard"] for image in details["Images"]]
        sku = []

        for size in sizes[1:]:
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

        return self.has_more_colors(response, response.meta["colors"], loader)

    def parse_product(self, response):
        loader = LindexItemLoader(item=LindexItem(), response=response)
        loader.add_value("uuid", self.extract_uuid(response))
        loader.add_value("retailer_sku", self.extract_retailer_sku(response))
        loader.add_value("industry", self.extract_industry(response))
        loader.add_value("name", self.extract_name(response))
        loader.add_value("brand", self.extract_brand(response))
        loader.add_value("price", self.extract_price(response))
        loader.add_value("currency", self.extract_currency(response))
        loader.add_value("gender", "Women")
        loader.add_value("category", self.extract_category(response))
        loader.add_value("description", self.extract_description_text(response))
        loader.add_value("care", self.extract_care(response))
        loader.add_value("url_orignal", response.url)
        loader.add_value("url", self.extract_url(response))
        loader.add_value("date", datetime.now().strftime("%Y-%m-%d"))
        loader.add_value("market", self.extract_market(response))
        loader.add_value("retailer", "lindex-uk")
        loader.add_value("spider_name", "lindex-uk-crawl")
        loader.add_value("crawl_id", f"lindex-uk-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj")
        loader.add_value("crawl_start_time", datetime.now().isoformat())

        colors = self.extract_colors(response)
        yield scrapy.Request(
            url="https://www.lindex.com/WebServices/ProductService.asmx/GetProductData",
            headers={
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/json; charset=UTF-8",
                },
            method="POST",
            body=json.dumps({
                "productIdentifier": self.extract_product_id(response),
                "colorId": colors.pop(0),
                "primaryImageType": "1"
                }),
            meta={"loader": loader, "colors": colors},
            callback=self.skus
            )

    def extract_uuid(self, response):
        return response.css(".main_content::attr(data-productid)").extract()

    def extract_name(self, response):
        return response.css(".name::text").extract()

    def extract_retailer_sku(self, response):
        return response.css(
            ".main_content .product_placeholder::attr(data-product-identifier)"
            ).extract()

    def extract_industry(self, response):
        return response.css(
            ".main_content .product_placeholder::attr(data-style)"
        ).extract()

    def extract_brand(self, response):
        return response.css(
            ".main_content .product_placeholder::attr(data-product-brand)"
        ).extract()

    def extract_price(self, response):
        return response.css(
            ".main_content .product_placeholder::attr(data-product-price)"
        ).extract()

    def extract_currency(self, response):
        return response.css(".totalPrice::text").extract()

    def extract_category(self, response):
        return response.css(
            ".main_content .product_placeholder::attr(data-product-category)"
        ).extract()

    def extract_description_text(self, response):
        return response.css(".description ::text").extract()

    def extract_care(self, response):
        return response.css(".more_info ::text").extract()

    def extract_url(self, response):
        return response.css("link[rel='canonical']::attr(href)").extract()

    def extract_market(self, response):
        return response.css(
            ".selectedCountry[type='hidden']::attr(value)").extract()
