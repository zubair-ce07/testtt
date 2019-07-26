import re
import scrapy

from datetime import datetime


class AsicsSpider(scrapy.Spider):
    name = 'asics'
    start_urls = ['https://www.asics.com']

    def parse(self, response):
        urls = response.css(".navNodeImageContainer a::attr(href)").getall()
        for url in urls:
            category = response.urljoin(url)
            yield scrapy.Request(category, callback=self.parse_category)

    def parse_category(self, response):
        products = response.css(".prod-wrap a::attr(href)").getall()
        gender = response.css(".prod-wrap a::attr(data-product-gender)").get()
        category = response.css(".prod-wrap a::attr(data-category)").get()
        for product in products:
            product_url = response.urljoin(product)
            yield scrapy.Request(product_url, callback=self.parse_product, meta={"gender": gender, "category": category})
        next_page = response.css("#nextPageLink a::attr(href)").get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_category)

    @staticmethod
    def parse_sku(response):
        sku_key = []
        sku_size = []
        sku_price = []
        sku_currency = []
        product = response.meta["product"]
        requests = response.meta["requests"]
        sku = response.css(".desktop-style")
        if not sku:
            sku = response.css(".dropdown")
        color_code = response.css(".tfc-fitrec-product::attr(data-colorid)").get()
        color = response.xpath("//a[contains(@href,'"+color_code+"')]").css("::attr(title)").get()
        for i in range(0, len(sku)):
            size_option = sku[i].css("a.SizeOption::text").getall()
            sku_size = [re.sub('\s+', '', s) for s in size_option if s.strip()]
            if sku_size:
                sku_key = sku[i].css(".SizeOption::attr(data-value)").getall()
                sku_currency = sku[i].css(".SizeOption meta[itemprop=priceCurrency]::attr(content)").getall()
                sku_price = sku[i].css(".SizeOption meta[itemprop=price]::attr(content)").getall()
                break

        skus = list(zip(sku_key, sku_currency, sku_price, sku_size))
        sku_result = {}
        for sku in skus:
            val = {
                "color": color,
                "currency": sku[1],
                "price": sku[2],
                "size": sku[3]
            }
            sku_result[sku[0]] = val
            product["skus"].update(sku_result)
        if requests:
            req = requests.pop()
            req.meta["product"] = product
            req.meta["requests"] = requests
            yield req
        else:
            yield product

    def parse_product(self, response):
        brand = "ASICS"
        date = datetime.now().timestamp()
        gender = response.meta["gender"]
        category = response.meta["category"]
        currency = response.css("#page::attr(data-currency-iso-code)").get()
        market = response.css("#countrycode::attr(value)").get()
        name = response.css(".single-prod-title::text").get()
        description = response.css("#collapse1::text").get()
        if not description:
            description = response.css("meta[property='og:description']::attr(content)").get()
        price = response.css("p.price meta[itemprop=price]::attr(content)").get()
        images = response.css(".product-img::attr(data-url-src)").getall()

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
            "skus": {}
        }
        colors_url = response.css(".col-sm-4 a.colorVariant::attr(href)").getall()
        requests = []
        for sku_color in colors_url:
            color_url = response.urljoin(sku_color)
            requests.append(scrapy.Request(color_url, self.parse_sku, dont_filter=True))
        if requests:
            req = requests.pop()
            req.meta["product"] = product
            req.meta["requests"] = requests
            yield req

