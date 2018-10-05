# -*- coding: utf-8 -*-
import re
import math
import scrapy
from scrapy.http.cookies import CookieJar
from greatfoodhallbot.items import GreatFoodHallProduct


class GreatfoodhallSpider(scrapy.Spider):
    name = 'greatfoodhall'
    allowed_domains = ['www.greatfoodhall.com']
    start_urls = ['http://www.greatfoodhall.com/eshop/LoginPage.do']

    def parse(self, response):
        category_links = response.css(
            "div.mainNav ul li.m6 a::attr(href)"
            ).re(r'ShowProductPage.do\?.+')

        for i, link in enumerate(category_links):
            yield scrapy.Request(
                url=self.start_urls[0],
                callback=self.request_with_new_cookie,
                meta={"cate_link": link, "cookiejar": i},
                dont_filter=True
            )

    def request_with_new_cookie(self, response):
        link = response.meta["cate_link"]

        yield scrapy.Request(
            url=response.urljoin(link),
            meta={
                "cookiejar": response.meta["cookiejar"],
                "total_products": 0
                },
            dont_filter=True,
            callback=self.parse_products
            )

    def parse_products(self, response):
        products_link = response.css(
            "div.productItems div.productTmb a::attr(href)"
            ).extract()

        for product in products_link:
            yield scrapy.Request(
                url=product,
                meta={"cookiejar": response.meta["cookiejar"]},
                dont_filter=True,
                callback=self.parse_product_details,
            )

        # pagination

        total_products = int(response.meta["total_products"])
        if total_products == 0:
            total_products = response.css("b.totalItem::text").extract_first()
        if total_products is not None:
            total_page = math.ceil(int(total_products) / 9)
            if 'curPage_' in response.url:
                curr_page = int(
                    re.search(r'curPage_\d+=(\d+)', response.url).group(1)
                    )
                if curr_page < total_page:
                    curr_page += 1
                    next_page = re.sub(
                        r'curPage_\d+=(\d+)', 'curPage_1=' +
                        str(curr_page), response.url
                        )
                    yield scrapy.Request(
                        url=next_page,
                        meta={
                            "cookiejar": response.meta["cookiejar"],
                            "total_products": total_products
                            },
                        dont_filter=True,
                        callback=self.parse_products,
                    )
            else:
                next_page = "http://www.greatfoodhall.com/eshop/ShowProductPage.do?curPage_1=2"
                yield scrapy.Request(
                    url=next_page,
                    meta={
                        "cookiejar": response.meta["cookiejar"],
                        "total_products": total_products
                    },
                    dont_filter=True,
                    callback=self.parse_products,
                )

    def parse_product_details(self, response):
        product = GreatFoodHallProduct()
        product["brand"] = 'GreatFoodHall'
        product["name"] = response.css(
            "p.description.pB5.pL6.typeface-js::text"
            ).extract_first()
        category = response.xpath(
            "//*[@id='form_Product']/div[2]/div[1]/div/ul/li/a/text()"
            ).extract()

        category = [i.strip('\n ') for i in category if i is not ' ']
        if category[0]:
            product["category"] = category[0]
        # response.css("div.middleArea h1::text").extract_first()
        product["description"] = response.css(
            "div#nutrition td::text"
            ).extract_first()
        product["image_urls"] = response.css(
            "div.productPhoto img::attr(src)"
            ).extract_first()
        product["url"] = response.url

        yield product
