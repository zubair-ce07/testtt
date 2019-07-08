import scrapy
import json
import re


class ProductSpider(scrapy.Spider):
    name = "product"

    def start_requests(self):
        url = 'https://www.apc-us.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.css(".item .go_page::attr(href)").getall():
            yield response.follow(url, callback=self.parse)

        for url in response.css(".item::attr(href)").getall():
            yield response.follow(url, callback=self.fetch_item_details)

        for url in response.css(".pagination a::attr(href)").getall():
            yield response.follow(url, callback=self.parse)

    def fetch_item_details(self, response):
        product = self.get_script_json(response)
        product_attr = {
            "name": self.get_name(product),
            "category": self.get_category(response),
            "description":  self.get_description(response),
            "image_urls": self.get_image_urls(response),
            "brand":  self.get_brand(response),
            "retailer_sku": self.get_retailer_sku(product),
            "url": self.get_url(response),
            "gender": self.get_gender(product),
            "skus": self.get_skus(response, product)
        }
        yield product_attr

    def get_name(self, product):
        return product["title"]

    def get_category(self, response):
        return response.css(".breadcrumbs a::text").getall()

    def get_description(self, response):
        return response.css(".description i::text").get() or response.css(".description p::text").get() or \
               response.css(".description span::text").get() or response.css(".description .ellipsis::text").get() or \
               response.css(".description::text").get()

    def make_img_url(self, response):
        for img_url in response.css("::attr(data-zoom-img)").getall():
            yield response.follow(img_url, None).url

    def get_image_urls(self, response):
        image_urls = []
        for url in self.make_img_url(response):
            image_urls.append(url)
        return image_urls

    def get_brand(self, response):
        return "A.P.C"

    def get_retailer_sku(self, product):
        return product["id"]

    def get_url(self, response):
        return response.url

    def get_script_json(self, response):
        return json.loads(response.css("script[data-product-json]::text").get())

    def get_gender(self, product):
        gender_attribute = [attribute for attribute in product["tags"] if "Gender" in attribute]
        if gender_attribute:
            return re.split('\\bGender:\\b', gender_attribute[0])[-1]

    def get_skus(self, response, product):
        skus = []
        for variant in product["variants"]:
            skus.append({
                "sku_id": variant["id"],
                "color": variant["option1"],
                "currency": self.get_currency(response),
                "size": variant["option2"],
                "out_of_stock": not variant["available"],
                "price": variant["price"],
                "previous_price": self.get_prev_price(variant)
            })
        return skus

    def get_prev_price(self, variant):
        if isinstance(variant["compare_at_price"], list):
            return variant["compare_at_price"]
        prev_price = []
        prev_price.append(variant["compare_at_price"])
        return prev_price

    def get_currency(self, response):
        return response.css("::attr(data-currency)").get()
