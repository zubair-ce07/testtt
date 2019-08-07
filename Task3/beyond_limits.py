# -*- coding: utf-8 -*-
import scrapy

from ..items import Product


class BeyondLimitsSpider(scrapy.Spider):
    name = 'beyondlimits'

    CSSPATH_PRODUCT = ".bb_details"
    CSSPATH_PRODUCT_NAME = ".bb_art--title::text"
    CSSPATH_PRODUCT_SKU = ".bb_art--artnum span::text"
    CSSPATH_PRODUCT_PRICE = ".price span::attr(content)"
    CSSPATH_PRODUCT_CURRENCY = ".price meta::attr(content)"
    CSSPATH_PRODUCT_SIZE = ".bb_form--select option::text"
    CSSPATH_PRODUCT_DESCRIPTION = "#description p::text"
    CSSPATH_PRODUCT_DESCRIPTION_2 = "#description::text"
    CSSPATH_PRODUCT_MATERIAL = "tr:nth-child(1) .data::text"
    CSSPATH_PRODUCT_IMAGES = ".bb_pic--navlink ::attr(href)"
    CSSPATH_PRODUCT_CARE = "#description li::text"
    CSSPATH_PRODUCT_META = "head meta[name=keywords]::attr(content)"
    CSSPATH_PRODUCT_CATEGORY = "strong::text"
    CSSPATH_GENDER = ".bb_breadcrumb--div+ .bb_breadcrumb--item span::text"

    allowed_domains = ['beyondlimits.com']
    start_urls = ['https://www.beyondlimits.com/']

    def is_url_valid(self, url):
        return not "de/" in url

    def parse(self, response):

        links = response.css("a::attr(href)")
        product = response.css(self.CSSPATH_PRODUCT)
        if product:
            product_item = Product()
            product_item['name'] = response.css(self.CSSPATH_PRODUCT_NAME).get()
            product_item['retailer_sku'] = response.css(self.CSSPATH_PRODUCT_SKU).get()
            product_item['brand'] = "BeyondLimits"
            product_item['lang'] = "en"
            description = response.css(self.CSSPATH_PRODUCT_DESCRIPTION).getall()
            if not description:
                description.append(response.css(self.CSSPATH_PRODUCT_DESCRIPTION_2).get())
            product_item['description'] = description
            
            product_tips = response.css(self.CSSPATH_PRODUCT_CARE).getall()
            product_item['image_urls'] = response.css(self.CSSPATH_PRODUCT_IMAGES).getall()
            
            gender = response.css(self.CSSPATH_GENDER).get()
            category = response.css(self.CSSPATH_PRODUCT_CATEGORY).get()
            if category in ('Men', 'Women'):
                gender, category = category, gender
            product_item['gender'] = gender
            product_item['category'] = category
            product_item['url'] = response.request.url
            product_price = response.css(self.CSSPATH_PRODUCT_PRICE).get()
            currency = response.css(self.CSSPATH_PRODUCT_CURRENCY).get()
            product_sizes = response.css(self.CSSPATH_PRODUCT_SIZE).getall()
            if product_sizes:
                del product_sizes[0]
            product_care = []
            product_colors = []

            for tip in product_tips:
                if "Care" in tip or "Material" in tip:
                    product_care.append(tip)
                if "Colour" in tip:
                    product_colors = tip.replace("Colour: ", "").split(",")
            product_item['care'] = product_care
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
            product_item['skus'] = skus
            yield product_item

        for link in links:
            if self.is_url_valid(link.get()):
                yield response.follow(link, self.parse)
