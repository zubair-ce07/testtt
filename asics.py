import re

from scrapy import Spider, Request
from datetime import datetime


class AsicsSpider(Spider):
    name = "asics"
    allowed_domains = ["asics.com", "onitsukatiger.com"]
    start_urls = ["https://www.asics.com"]

    def parse(self, response):
        urls = response.css(".navNodeImageContainer a::attr(href)").getall()
        yield from [Request(response.urljoin(url), callback=self.parse_category) for url in urls]

    def parse_category(self, response):
        products = response.css(".prod-wrap a::attr(href)").getall()
        gender = response.css(".prod-wrap a::attr(data-product-gender)").get()
        category = response.css(".prod-wrap a::attr(data-category)").get()
        gender_category = {"gender": gender, "category": category}
        yield from [Request(response.urljoin(product),
                            callback=self.parse_product,
                            meta=gender_category)
                    for product in products]
        next_page = response.css("#nextPageLink a::attr(href)").get()

        if next_page:
            yield Request(response.urljoin(next_page), callback=self.parse_category)

    def parse_product(self, response):
        requests = []
        brand = response.css("html::attr(data-brand)").get()
        date = datetime.now().timestamp()
        gender = response.meta["gender"]
        category = response.meta["category"]
        currency = response.css("#page::attr(data-currency-iso-code)").get()
        market = response.css("#countrycode::attr(value)").get()
        name = response.css(".single-prod-title::text").get()
        description = response.css("meta[property='og:description']::attr(content)").get()
        price = response.css("p.price meta[itemprop=price]::attr(content)").get()
        images = response.css(".product-img::attr(data-big)").getall()
        skus = self.extract_skus(response)
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
            "skus": skus
        }
        colors_url_css = "#variant-choices div:not([class*='active']) a::attr(href)"
        colors_url = response.css(colors_url_css).getall()

        for sku_color in colors_url:
            color_url = response.urljoin(sku_color)
            requests.append(Request(color_url, self.parse_color))
        yield from self.get_product(requests, product)

    def parse_color(self, response):
        product = response.meta["product"]
        requests = response.meta["requests"]
        sku_result = self.extract_skus(response)
        product["skus"].update(sku_result)
        yield from self.get_product(requests, product)

    def extract_skus(self, response):
        return self.extract_skus_primary(response) if self.start_urls[0] in response.url \
            else self.extract_skus_secondary(response)

    @staticmethod
    def extract_skus_primary(response):

        sku_result = {}
        color = response.css("#variant-choices .active img::attr(title)").get()

        for sku_sel in response.css(".tab-content .tab:not(.hide-tab)"
                                    " .size-box-select-container .size-select-list div"):
            size = clean_data(str(sku_sel.css("a.SizeOption::text").get()))
            if not size:
                continue

            sku_key = sku_sel.css("::attr(data-value)").get()
            sku_currency = sku_sel.css("meta[itemprop=priceCurrency]::attr(content)").get()
            sku_price = sku_sel.css("meta[itemprop=price]::attr(content)").get()
            sku_result[sku_key] = {
                "color": color,
                "currency": sku_currency,
                "price": sku_price,
                "size": size
            }

        return sku_result

    @staticmethod
    def extract_skus_secondary(response):
        sku_result = {}
        color = response.css("#variant-choices .active img::attr(title)").get()

        for sku_sel in response.css("#SelectSizeDropDown li"):
            size = clean_data(str(sku_sel.css("a.SizeOption::text").get()))

            if not size:
                continue

            sku_key = sku_sel.css("::attr(data-value)").get()
            sku_currency = sku_sel.css("meta[itemprop=priceCurrency]::attr(content)").get()
            sku_price = sku_sel.css("meta[itemprop=price]::attr(content)").get()
            sku_result[sku_key] = {
                "color": color,
                "currency": sku_currency,
                "price": sku_price,
                "size": size
            }

        return sku_result

    @staticmethod
    def get_product(requests, product):

        if requests:
            req = requests.pop()
            req.meta["product"] = product
            req.meta["requests"] = requests
            yield req
        else:
            yield product


def clean_data(to_clean):
    return re.sub('\s+', '', to_clean)

