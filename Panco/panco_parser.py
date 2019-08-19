# -*- coding: utf-8 -*-
import json

import scrapy

from ..items import Product

class PancoParserSpider(scrapy.Spider):
    name = 'panco_parser'
    allowed_domains = ['panco.com']
    start_urls = ['https://www.panco.com.tr']
    possible_genders = ['Yenidoğan', 'Kiz Bebek', 'Kiz Çocuk', 'Erkek Bebek', 'Erkek Çocuk']

    def parse_product(self, response):
        product_item = Product()
        raw_product = json.loads(response.css(".js-main-wrapper .analytics-data::text").get())
        product_item['name'] = response.css(".product-name::text").get()
        product_item['retailer_sku'] = response.css(".product-number::text").get()
        product_item['brand'] = raw_product['productDetail']['data']['brand']
        product_item['lang'] = response.css("html::attr(lang)").get()
        product_item['description'] = response.css(".js-product-content__tab--delivery div.content::text").get().strip()
        product_item['image_urls'] = response.css(".js-product-slider__main img::attr(src)").getall()
        product_item['category'] = self.get_category(response)
        product_item['gender'] = self.get_gender(response)
        product_item['url'] = response.request.url
        product_item['skus'] = self.get_skus(response)
        return product_item

    def get_category(self, response):
        return response.css(".breadcrumb a::text, .breadcrumb span::text").getall()[1:]

    def get_gender(self, response):
        category = ' '.join(self.get_category(response))
        for gender in self.possible_genders:
            if gender.lower() in category.lower():
                return gender

    def get_skus(self, response):
        raw_product = json.loads(response.css(".js-main-wrapper .analytics-data::text").get())
        product_price = raw_product['productDetail']['data']['price']
        old_prices = [raw_product['productDetail']['data']['dimension16']]
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
                    "previous_prices": old_prices
                }
                skus[f"{color}_{size}"] = sku
        return skus
