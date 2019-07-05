import scrapy
import json


class ProductSpider(scrapy.Spider):
    name = "product"

    def start_requests(self):
        url = 'https://www.apc-us.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.css(".toggle_promo_collection::attr(href)")\
         .getall():
            yield response.follow(url, callback=self.parse)

        for url in response.css(".item-33 a::attr(href)").getall():
            yield response.follow(url, callback=self.parse)

        for url in response.css(".item::attr(href)").getall():
            yield response.follow(url, callback=self.fetch)

        for url in response.css(".justify-center a::attr(href)").getall():
            yield response.follow(url, callback=self.parse)

        for url in response.css(".colorama-product-link-wrapper::attr(href)")\
         .getall():
            yield response.follow(url, callback=self.fetch)

    def fetch(self, response):
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
        return product.get("title")

    def get_category(self, response):
        return response.css(".breadcrumbs a::text").getall()

    def get_description(self, response):
        return response.css(".description i::text").get() or \
               response.css(".description p::text").get() or \
               response.css(".description span::text").get() or \
               response.css(".description .ellipsis::text").get() or \
               response.css(".description::text").get()

    def get_image_urls(self, response):
        return response.css(".swiper-slide img::attr(src)").getall()

    def get_brand(self, response):
        return "".join(response.css(".logo span::text").getall())

    def get_retailer_sku(self, product):
        return product.get("id")

    def get_url(self, response):
        return response.url

    def get_script_json(self, response):
        return json.loads(response.css("script[data-product-json]::text")
                          .get())

    def get_gender(self, product):
        for attribute in product.get("tags"):
            if attribute.find("Gender:") != -1:
                return attribute.replace("Gender:", "")

    def get_skus(self, response, product):
        skus = []
        for variant in product.get("variants"):
            skus.append({
                "sku_id": variant.get("id"),
                "color": variant.get("option1"),
                "currency": self.get_currency(response),
                "size": variant.get("option2"),
                "out_of_stock": str(not variant.get("available")).lower(),
                "price": variant.get("price"),
                "previous_price": variant.get("compare_at_price"),
            })
        return skus

    def get_currency(self, response):
        currency = ""
        product_attr = response.css("script.analytics").get()
        for i in range(product_attr.find("\"currency"), len(product_attr)):
            if product_attr[i] == ",":
                break
            currency += product_attr[i]
        return currency.replace("\"currency\":\"", "")
