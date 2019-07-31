import re
from datetime import datetime

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AsicsSpider(CrawlSpider):
    name = "asics"
    allowed_domains = ["asics.com", "onitsukatiger.com"]
    start_urls = ["https://www.asics.com"]

    rules = [
        Rule(LinkExtractor(restrict_css=".navNodeImageContainer"), callback="parse_category")
    ]

    def parse_category(self, response):
        products = response.css(".prod-wrap a::attr(href)").getall()
        gender = response.css(".prod-wrap a::attr(data-product-gender)").get()
        category = response.css(".prod-wrap a::attr(data-category)").get()
        parameters = {
            "meta": {"gender": gender, "category": category},
            "callback": self.parse_product,
        }
        yield from [Request(response.urljoin(product), **parameters) for product in products]

        next_page = response.css("#nextPageLink a::attr(href)").get()
        if next_page:
            yield Request(response.urljoin(next_page), callback=self.parse_category)

    def parse_product(self, response):
        brand = response.css("html::attr(data-brand)").get()
        category = response.meta["category"]
        currency = response.css("#page::attr(data-currency-iso-code)").get()
        date = datetime.now().timestamp()
        description = response.css("meta[property='og:description']::attr(content)").get()
        gender = response.meta["gender"]
        images = response.css(".product-img::attr(data-big)").getall()
        market = response.css("#countrycode::attr(value)").get()
        name = response.css(".single-prod-title::text").get()
        price = response.css("p.price meta[itemprop=price]::attr(content)").get()
        skus = self.extract_skus(response)
        product = {
            "brand": brand,
            "category": category,
            "currency": currency,
            "date": date,
            "description": description,
            "gender": gender,
            "img_urls": images,
            "lang": "en",
            "market": market,
            "name": name,
            "price": price,
            "skus": skus
        }
        color_urls_css = "#variant-choices div:not([class*='active']) a::attr(href)"
        color_urls = response.css(color_urls_css).getall()
        requests = [Request(response.urljoin(url), self.parse_color) for url in color_urls]
        yield from self.get_request_or_product(requests, product)

    def parse_color(self, response):
        product = response.meta["product"]
        requests = response.meta["requests"]
        skus = self.extract_skus(response)
        product["skus"].update(skus)
        yield from self.get_request_or_product(requests, product)

    @staticmethod
    def extract_skus(response):
        skus = {}
        color = response.css("#variant-choices .active img::attr(title)").get()
        sku_css = ".tab-content .tab:not(.hide-tab) .size-box-select-container .size-select-list div"

        if "asics.com" not in response.url:
            sku_css = "#SelectSizeDropDown li"

        for sku_sel in response.css(sku_css):
            size = clean(sku_sel.css("a.SizeOption::text").get())
            if not size:
                continue

            sku_key = sku_sel.css("::attr(data-value)").get()
            sku_currency = sku_sel.css("meta[itemprop=priceCurrency]::attr(content)").get()
            sku_price = sku_sel.css("meta[itemprop=price]::attr(content)").get()
            skus[sku_key] = {
                "color": color,
                "currency": sku_currency,
                "price": sku_price,
                "size": size
            }

        return skus

    @staticmethod
    def get_request_or_product(requests, product):
        if requests:
            request = requests.pop()
            request.meta["product"] = product
            request.meta["requests"] = requests
            return request

        yield product


def clean(raw_text):
    if raw_text:
        return re.sub('\s+', '', raw_text)
