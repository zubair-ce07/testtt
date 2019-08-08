# -*- coding: utf-8 -*-
import scrapy

from ..items import Product

class BeyondLimitsSpider(scrapy.Spider):
    name = 'beyondlimits'

    possible_genders = ['Men', 'Women']
    allowed_domains = ['beyondlimits.com']
    start_urls = ['https://www.beyondlimits.com/']

    def parse_product(self, response):
        product_item = Product()
        product_item['name'] = response.css(".bb_art--title::text").get()
        product_item['retailer_sku'] = response.css(".bb_art--artnum span::text").get()
        product_item['brand'] = "BeyondLimits"
        product_item['lang'] = "en"
        product_item['description'] = self.get_product_description(response)
        product_item['image_urls'] = response.css(".bb_pic--navlink ::attr(href)").getall()
        product_item['gender'] = self.get_gender(response)
        product_item['category'] = self.get_category(response)
        product_item['url'] = response.request.url
        product_item['care'] = self.get_care(response)
        product_item['skus'] = self.get_skus(response)
        return product_item

    def is_url_valid(self, url):
        return not "/de/" in url

    def get_product_description(self, response):
        description = response.css("#description p::text, #description::text").getall()
        return description

    def get_gender(self, response):
        category = ''.join(self.get_category(response))
        for gender in self.possible_genders:
            if gender in category:
                return gender

    def get_category(self, response):
        categories = response.css(".bb_breadcrumb--item span::text, .bb_breadcrumb--item strong::text").getall()
        if categories:
            del categories[0]
        return categories

    def get_care(self, response):
        description_list = response.css("#description li::text").getall()
        product_care = []
        for product_feature in description_list:
            if any(care in product_feature for care in ["Care", "Material"]):
                product_care.append(product_feature)
        return product_care

    def get_colours(self, response):
        description_list = response.css("#description li::text").getall()
        colours = []
        for product_feature in description_list:
            if "Colour" in product_feature:
                colours = product_feature.replace("Colour: ", "").split(",")
        return colours

    def get_skus(self, response):
        product_price = response.css(".price span::attr(content)").get()
        currency = response.css(".price meta::attr(content)").get()
        product_sizes = response.css(".bb_form--select option::text").getall()
        if product_sizes:
            del product_sizes[0]
        product_colors = self.get_colours(response)
        skus = {}
        for color in product_colors:
            for size in product_sizes:
                sku =	{
                    "colour": color,
                    "pirce": product_price,
                    "currency": currency,
                    "size": size
                }
                skus[f"{color}_{size}"] = sku
        return skus

    def parse(self, response):

        links = response.css("a::attr(href)")
        product = response.css(".bb_details")
        if product:
            yield self.parse_product(response)

        for link in links:
            if self.is_url_valid(link.get()):
                yield response.follow(link, self.parse)

