import scrapy
import json


class ProductSpider(scrapy.Spider):
    name = "product"

    def start_requests(self):
        url = 'https://www.apc-us.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.css(".item a::attr(href)").extract():
            yield response.follow(url, callback=self.parse)

        for url in response.css(".item::attr(href)").extract():
            yield response.follow(url, callback=self.fetch)

        for url in response.css(".justify-center a::attr(href)").extract():
            yield response.follow(url, callback=self.parse)

        new_urls = response.css(".colorama-product-link-wrapper::attr(href)")
        for url in new_urls.extract():
            yield response.follow(url, callback=self.fetch)

    def fetch(self, response):
        product = json.loads(response.css("script[data-product-json]::text")
                             .get())
        gender = ""
        for attribute in product.get("tags"):
            if attribute.find("Gender:") == 0:
                gender = attribute
        product_attr = {
            "name": product.get("title"),
            "category": response.css(".breadcrumbs a::text").extract(),
            "description":  response.css(".description p::text").extract(),
            "image_urls": response.css(".swiper-slide img::attr(src)").
            extract(),
            "brand":  "".join(response.css(".logo span::text").extract()),
            "retailer_sku": product.get("id"),
            "url": response.url,
            "gender": gender
        }

        yield product_attr
