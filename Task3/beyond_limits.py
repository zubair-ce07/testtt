# -*- coding: utf-8 -*-
import scrapy

from ..items import Product

class BeyondLimitsSpider(scrapy.Spider):
    name = 'beyondlimits'

    allowed_domains = ['beyondlimits.com']
    start_urls = ['https://www.beyondlimits.com/']

    def is_url_valid(self, url):
        return not "de/" in url

    def get_product_description(self, response):
        description = response.css("#description p::text").getall()
        if not description:
            description.append(response.css("#description::text").get())
        return description

    def get_category_gender(self, response):
        gender = response.css(".bb_breadcrumb--div+ .bb_breadcrumb--item span::text").get()
        category = response.css("strong::text").get()
        if category in ('Men', 'Women'):
            gender, category = category, gender
        return category, gender

    def get_care_skus(self, response):
        product_tips = response.css("#description li::text").getall()
        product_price = response.css(".price span::attr(content)").get()
        currency = response.css(".price meta::attr(content)").get()
        product_sizes = response.css(".bb_form--select option::text").getall()
        if product_sizes:
            del product_sizes[0]
        product_care = []
        product_colors = []

        for tip in product_tips:
            if "Care" in tip or "Material" in tip:
                product_care.append(tip)
            if "Colour" in tip:
                product_colors = tip.replace("Colour: ", "").split(",")

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
        return product_care, skus

    def get_product(self, response):

        product_item = Product()
        product_item['name'] = response.css(".bb_art--title::text").get()
        product_item['retailer_sku'] = response.css(".bb_art--artnum span::text").get()
        product_item['brand'] = "BeyondLimits"
        product_item['lang'] = "en"
        product_item['description'] = self.get_product_description(response)
        product_item['image_urls'] = response.css(".bb_pic--navlink ::attr(href)").getall()
        category, gender = self.get_category_gender(response)
        product_item['gender'] = gender
        product_item['category'] = category
        product_item['url'] = response.request.url
        care, skus = self.get_care_skus(response)
        product_item['care'] = care
        product_item['skus'] = skus
        return product_item

    def parse(self, response):

        links = response.css("a::attr(href)")
        product = response.css(".bb_details")
        if product:
            yield self.get_product(response)

        for link in links:
            if self.is_url_valid(link.get()):
                yield response.follow(link, self.parse)

