import json
import re

import scrapy
from greatfoodhall.items import GreatfoodhallItem, GreatfoodhallLoader
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import (DNSLookupError, TCPTimedOutError,
                                    TimeoutError)


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['www.greatfoodhall.com']
    start_urls = ['http://www.greatfoodhall.com/eshop/LoginPage.do']

    selectors = {
        "category_urls": ".item a::attr(href)",
        "product_urls": ".productTmb a::attr(href)",
        "name": ".description::text",
        "image": ".productPhoto img::attr(src)",
        "flag_image": ".flag::attr(src)",
        "price": ".itemOrgPrice2::text",
        "nutrition_info_values": "#nutrition table tr td[align=right]::text",
        "nutrition_info_fields": "#nutrition table tr td[align=left]::text",
        "quantity": ".ml::text",
        "categories": ".breadCrumbArea ul::text",
        "product_type": "h1.pL6::text",
        "availability": ".btnAddToCart img"
    }

    def parse(self, response):
        """Requests the main page url for each category
        for setting the cookies"""
        category_urls = self.get_category_urls(response)

        for cookie_identfier, url in enumerate(category_urls):
            yield scrapy.Request(
                url="http://www.greatfoodhall.com/eshop/LoginPage.do",
                callback=self.parse_category,
                errback=self.errback_httpbin,
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
            errback=self.errback_httpbin,
            meta={
                "cookiejar": response.meta["cookiejar"],
                "current_page": 1,
            }
        )

    def get_total_pages(self, response):
        """Return total pages for each category"""
        total_pages = re.findall(
            r'\d+',
            re.findall(r'totalpage = (.*)', response.text)[0])[0]
        return int(total_pages)

    def parse_list(self, response):
        """Getting the product urls for each page and
        specific category and request for parsing"""
        product_urls = self.get_product_urls(response)
        for url in product_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_product,
                errback=self.errback_httpbin,
                meta={'cookiejar': response.meta["cookiejar"]},
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
                errback=self.errback_httpbin,
                meta={
                    'cookiejar': response.meta["cookiejar"],
                    'total_pages': total_pages,
                    'current_page': response.meta["current_page"] + 1},
                dont_filter=True
            )

    def parse_product(self, response):
        """Item Loader implementation for products"""
        l = GreatfoodhallLoader(item=GreatfoodhallItem(), response=response)
        l.add_value("_id", re.findall(r"sp=(.*)", response.url)[0])
        l.add_css("name", self.selectors["name"])
        l.add_css("price", self.selectors["price"])
        l.add_value('currency', 'Hong Kong dollar (HK$)')
        l.add_css(
            "nutrition_info_values", self.selectors["nutrition_info_values"])
        l.add_css(
            "nutrition_info_fields", self.selectors["nutrition_info_fields"])
        l.add_css("quantity", self.selectors["quantity"])
        l.add_css("categories", self.selectors["categories"])
        l.add_css("product_type", self.selectors["product_type"])
        l.add_css("image_url", self.selectors["image"])
        l.add_css("flag_image", self.selectors["flag_image"])
        l.add_css("availability", self.selectors["availability"])
        l.add_value('website', 'http://www.greatfoodhall.com')
        l.add_value("url", response.url)
        return l.load_item()

    # Getters using CSS Selectors #

    def get_category_urls(self, response):
        category_urls = response.css(self.selectors["category_urls"]).extract()
        return [response.urljoin(url) for url in category_urls]

    def get_product_urls(self, response):
        return response.css(self.selectors["product_urls"]).extract()

    def errback_httpbin(self, failure):
        """Error back function for detecting the request errors"""
        # log all failures
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
