import re

from scrapy import Spider, Request
from datetime import datetime


class AsicsSpider(Spider):
    name = "asics"
    start_urls = ["https://www.asics.com"]

    def parse(self, response):
        urls = response.css(".navNodeImageContainer a::attr(href)").getall()
        for url in urls:
            category = response.urljoin(url)
            yield Request(category, callback=self.parse_category)

    def parse_category(self, response):
        products = response.css(".prod-wrap a::attr(href)").getall()
        gender = response.css(".prod-wrap a::attr(data-product-gender)").get()
        category = response.css(".prod-wrap a::attr(data-category)").get()
        for product in products:
            product_url = response.urljoin(product)
            yield Request(product_url, callback=self.parse_product, meta={"gender": gender, "category": category})
        next_page = response.css("#nextPageLink a::attr(href)").get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse_category)

    def parse_product(self, response):
        brand = response.css("html::attr(data-brand)").get()
        date = datetime.now().timestamp()
        gender = response.meta["gender"]
        category = response.meta["category"]
        currency = response.css("#page::attr(data-currency-iso-code)").get()
        market = response.css("#countrycode::attr(value)").get()
        name = response.css(".single-prod-title::text").get()
        description = response.css("meta[property='og:description']::attr(content)").get()
        price = response.css("p.price meta[itemprop=price]::attr(content)").get()
        images = response.css(".product-img::attr(data-url-src)").getall()

        if self.start_urls[0] in response.url:
            sku = AsicsSpider.generate_sku_first_domain(response)
        else:
            sku = AsicsSpider.generate_sku_second_domain(response)

        product = {
            "brand": brand,
            "category": category,
            "currency": currency,
            "date": date,
            "description": description.strip(),
            "gender": gender,
            "img_urls": images,
            "lang": "en",
            "market": market,
            "name": name,
            "price": price,
            "skus": sku
        }

        colors_url = response.css("#variant-choices div:not([class*='active']) a::attr(href)").getall()

        requests = []

        for sku_color in colors_url:
            color_url = response.urljoin(sku_color)
            requests.append(Request(color_url, self.parse_color))
        yield from AsicsSpider.check_requests(requests, product)

    def parse_color(self, response):
        product = response.meta["product"]
        requests = response.meta["requests"]
        if self.start_urls[0] in response.url:
            sku_result = AsicsSpider.generate_sku_first_domain(response)
        else:
            sku_result = AsicsSpider.generate_sku_second_domain(response)

        product["skus"].update(sku_result)
        yield from AsicsSpider.check_requests(requests, product)

    @staticmethod
    def generate_sku_second_domain(response):
        sku_result = {}
        raw_sku = response.css("#SelectSizeDropDown")
        size_option = raw_sku.css("a.SizeOption::text").getall()
        sku_size = clean_data(size_option)
        color = response.css("#variant-choices .active img::attr(title)").get()
        for index in range(1, len(sku_size) + 1):
            div = raw_sku.xpath(f"./li[{index}]")
            sku_key = div.css("::attr(data-value)").get()
            sku_currency = div.css("meta[itemprop=priceCurrency]::attr(content)").get()
            sku_price = div.css("meta[itemprop=price]::attr(content)").get()
            sku_result[sku_key] = {
                "color": color,
                "currency": sku_currency,
                "price": sku_price,
                "size": sku_size[index - 1]
            }
        return sku_result

    @staticmethod
    def generate_sku_first_domain(response):
        sku_size = []
        sku_result = {}
        raw_sku = response.css(".tab-content .tab:not(.hide-tab) .size-box-select-container .size-select-list")
        color = response.css("#variant-choices .active img::attr(title)").get()
        if raw_sku:
            raw_sku = raw_sku[0]
            size_option = raw_sku.css("a.SizeOption::text").getall()
            sku_size = clean_data(size_option)
        for index in range(1, len(sku_size) + 1):
            div = raw_sku.xpath(f"./div[{index}]")
            sku_key = div.css("::attr(data-value)").get()
            sku_currency = div.css("meta[itemprop=priceCurrency]::attr(content)").get()
            sku_price = div.css("meta[itemprop=price]::attr(content)").get()
            sku_result[sku_key] = {
                "color": color,
                "currency": sku_currency,
                "price": sku_price,
                "size": sku_size[index - 1]
            }
        return sku_result

    @staticmethod
    def check_requests(requests, product):
        if requests:
            req = requests.pop()
            req.meta["product"] = product
            req.meta["requests"] = requests
            yield req
        else:
            yield product


def clean_data(data):
    return [re.sub('\s+', '', datum) for datum in data if datum.strip()]

