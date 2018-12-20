import json
import re

import scrapy
from greatfoodhall.items import GreatfoodhallItem, GreatfoodhallLoader


class GreatFoodHallSpider(scrapy.Spider):
    name = "greatfoodhall"
    allowed_domains = ["www.greatfoodhall.com"]
    start_urls = ["http://www.greatfoodhall.com/eshop/LoginPage.do"]

    def parse(self, response):
        """Requests the main page url for each category
        for setting the cookies"""
        category_urls = self.get_category_urls(response)

        for cookie_identfier, url in enumerate(category_urls):
            yield scrapy.Request(
                url="http://www.greatfoodhall.com/eshop/LoginPage.do",
                callback=self.parse_category,
                meta={
                    "cookiejar": cookie_identfier,
                    "category_link": url},
                dont_filter=True
            )

    def parse_category(self, response):
        """Function for requesting the category urls"""
        yield scrapy.Request(
            url=response.meta["category_link"],
            callback=self.parse_list,
            meta={
                "cookiejar": response.meta["cookiejar"],
                "current_page": 1,
            }
        )

    def get_total_pages(self, response):
        """Return total pages for each category"""
        total_pages = re.findall(
            r"\d+",
            re.findall(r"totalpage = (.*)", response.text)[0])[0]
        return int(total_pages)

    def parse_list(self, response):
        """Getting the product urls for each page and
        specific category and request for parsing"""
        product_urls = self.get_product_urls(response)
        for url in product_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_product,
                meta={"cookiejar": response.meta["cookiejar"]},
            )

        if "total_pages" in response.meta:
            total_pages = response.meta["total_pages"]
        else:
            total_pages = self.get_total_pages(response)

        if response.meta["current_page"] < total_pages:
            yield scrapy.Request(
                url=response.urljoin(
                    "ShowProductPage.do?curPage_1={}".format(
                        response.meta["current_page"] + 1)),
                callback=self.parse_list,
                meta={
                    "cookiejar": response.meta["cookiejar"],
                    "total_pages": total_pages,
                    "current_page": response.meta["current_page"] + 1},
                dont_filter=True
            )

    def parse_product(self, response):
        """Item Loader implementation for products"""
        loader = GreatfoodhallLoader(item=GreatfoodhallItem(), response=response)
        loader.add_value("_id", re.findall(r"sp=(.*)", response.url)[0])
        loader.add_css("name", ".description::text")
        loader.add_css("price", ".itemOrgPrice2::text")
        loader.add_css('currency', ".itemOrgPrice2::text")
        loader.add_css(
            "nutrition_info_values",
            "#nutrition table tr td[align=right]::text")
        loader.add_css(
            "nutrition_info_fields",
            "#nutrition table tr td[align=left]::text")
        loader.add_css("quantity", ".ml::text")
        loader.add_css("categories", ".breadCrumbArea ul::text")
        loader.add_css("product_type", "h1.pL6::text")
        loader.add_css("image_url", ".productPhoto img::attr(src)")
        loader.add_css("flag_image", ".flag::attr(src)")
        loader.add_css("availability", ".btnAddToCart img")
        loader.add_value("website", "http://www.greatfoodhall.com")
        loader.add_value("url", response.url)
        return loader.load_item()

    def get_category_urls(self, response):
        category_urls = response.css(".item a::attr(href)").extract()
        return [response.urljoin(url) for url in category_urls]

    def get_product_urls(self, response):
        return response.css(".productTmb a::attr(href)").extract()
