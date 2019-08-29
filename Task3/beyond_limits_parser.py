# -*- coding: utf-8 -*-
import scrapy
import re

from ..items import Product

class BeyondParserSpider(scrapy.Spider):
    name = 'beyondlimits_parser'
    allowed_domains = ['beyondlimits.com']
    start_urls = ['https://www.beyondlimits.com/']
    possible_genders = ['Men', 'Women']

    def parse_product(self, response):
        product_item = Product()
        product_item['name'] = self.parse_name(response)
        product_item['retailer_sku'] = self.parse_retailer_sku(response)
        product_item['brand'] = "BeyondLimits"
        product_item['lang'] = "en"
        product_item['description'] = self.parse_product_description(response)
        product_item['image_urls'] = self.parse_image_urls(response)
        product_item['gender'] = self.parse_gender(response)
        product_item['category'] = self.parse_category(response)
        product_item['url'] = response.url
        product_item['care'] = self.parse_care(response)
        product_item['skus'] = self.parse_skus(response)

        return product_item

    def parse_name(self, response):
        return response.css(".bb_art--title::text").get()

    def parse_retailer_sku(self, response):
        return response.css(".bb_art--artnum span::text").get()

    def parse_product_description(self, response):
        return response.css("#description p::text, #description::text").getall()

    def parse_image_urls(self, response):
        return response.css(".bb_pic--navlink ::attr(href)").getall()

    def parse_gender(self, response):
        soup = ' '.join(self.parse_category(response))
        for gender in self.possible_genders:
            if gender.lower() in soup.lower():
                return gender

    def parse_category(self, response):
        categories_css = ".bb_breadcrumb--item span::text, .bb_breadcrumb--item strong::text"
        categories = response.css(categories_css).getall()
        return categories[1:]

    def parse_care(self, response):
        description_list = response.css("#description li::text").getall()
        product_care = []
        for product_feature in description_list:
            if any(care in product_feature for care in ["Care", "Material"]):
                product_care.append(product_feature)
        return product_care

    def parse_colours(self, response):
        description = " ".join(response.css("#description li::text").getall())
        return re.findall('Colour: (.*?) Care', description, re.DOTALL)

    def parse_skus(self, response):
        product_price = response.css(".price span::attr(content)").get()
        old_price = response.css(".oldPrice del::text").getall()
        currency = response.css(".price meta::attr(content)").get()
        product_sizes = response.css(".bb_form--select option::text").getall()[1:]
        product_colors = self.parse_colours(response)
        skus = {}
        for color in product_colors:
            for size in product_sizes:
                sku =	{
                    "colour": color,
                    "price": product_price,
                    "currency": currency,
                    "size": size
                }
                if old_price:
                    sku["privious_prices"] = old_price
                skus[f"{color}_{size}"] = sku
        return skus
