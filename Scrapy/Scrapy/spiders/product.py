import scrapy
import json


class ProductSpider(scrapy.Spider):
    name = "product"

    def start_requests(self):
        url = 'https://www.apc-us.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.css(".item a::attr(href)").getall():
            yield response.follow(url, callback=self.parse)

        for url in response.css(".item::attr(href)").getall():
            yield response.follow(url, callback=self.fetch)

        for url in response.css(".justify-center a::attr(href)").getall():
            yield response.follow(url, callback=self.parse)

        new_urls = response.css(".colorama-product-link-wrapper::attr(href)")
        for url in new_urls.getall():
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
            "gender": self.get_gender(product)
        }
        yield product_attr

    def get_name(self, product):
        return product.get("title")

    def get_category(self, response):
        return response.css(".breadcrumbs a::text").getall()

    def get_description(self, response):
        return response.css(".description p::text").get()

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
            if attribute.find("Gender:") == 0:
                return attribute
