# -*- coding: utf-8 -*-
import json

import scrapy
import w3lib.url

from ..items import Product

class PancoSpider(scrapy.Spider):
    name = 'panco'
    possible_genders = ['Yenidoğan', 'Kiz Bebek', 'Kiz Çocuk', 'Erkek Bebek', 'Erkek Çocuk']
    allowed_domains = ['panco.com.tr']
    start_urls = ['https://panco.com.tr/']

    def parse(self, response):
        links = response.css(".js-categories-carousel a::attr(href)")
        requests = [response.follow(link, self.parse_category) for link in links]
        return requests

    def parse_category(self, response):
        next_page = response.css(".paginate-bottom a.js-pagination-next::attr(href)").get()
        page_num = self.get_next_page(next_page)
        if page_num:
            url = w3lib.url.add_or_replace_parameter(response.request.url, 'page', page_num)
            yield response.follow(url, self.parse_category)

        products = response.css(".product-item-info a::attr(href)").getall()
        for product in products:
            yield response.follow(product, self.parse_product)

    def parse_product(self, response):
        product_item = Product()
        product_data = json.loads(response.css(".js-main-wrapper .analytics-data::text").get())
        product_item['name'] = response.css(".product-name::text").get()
        product_item['retailer_sku'] = response.css(".product-number::text").get()
        product_item['brand'] = product_data['productDetail']['data']['brand']
        product_item['lang'] = response.css("html::attr(lang)").get()
        product_item['description'] = response.css(".js-product-content__tab--delivery div.content::text").get().strip()
        product_item['image_urls'] = response.css(".js-product-slider__main img::attr(src)").getall()
        product_item['category'] = self.get_category(response)
        product_item['gender'] = self.get_gender(response)
        product_item['url'] = response.request.url
        product_item['skus'] = self.get_skus(response)
        return product_item

    def get_next_page(self, next_page):
        if next_page != "#":
            return next_page.split("?page=")[1]

    def get_category(self, response):
        return response.css(".breadcrumb a::text, .breadcrumb span::text").getall()[1:]

    def get_gender(self, response):
        category = ' '.join(self.get_category(response))
        for gender in self.possible_genders:
            if gender.lower() in category.lower():
                return gender

    def get_skus(self, response):
        product_data = json.loads(response.css(".js-main-wrapper .analytics-data::text").get())
        product_price = product_data['productDetail']['data']['price']
        old_price = product_data['productDetail']['data']['dimension16']
        currency = response.css("head meta[property='og:price:currency']::attr(content)").get()
        product_colors = response.css(".product-variant__item .variants-wrapper a::attr(data-value)").getall()
        product_sizes = response.css(".product-variant__item .product-size-item::attr(data-value)").getall()

        skus = {}
        for color in product_colors:
            for size in product_sizes:
                sku =	{
                    "colour": color,
                    "price": product_price,
                    "currency": currency,
                    "size": size,
                    "privious_prices": old_price
                }
                skus[f"{color}_{size}"] = sku
        return skus
