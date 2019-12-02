import re

import scrapy

from ..items import SnkrsItem


class SnkrsSpider(scrapy.Spider):
    name = 'snkrs'
    allowed_domains = ['snkrs.com']
    start_urls = ['http://snkrs.com/en/']
    product_id = set()

    def parse(self, response):
        urls = response.css('.a-niveau1::attr(href)').getall()
        yield from [response.follow(url, callback=self.parse_listing_page) for url in urls]

    def parse_listing_page(self, response):
        urls = response.css('.product_img_link::attr(href)').getall()
        yield from [response.follow(url, callback=self.parse_product_page) for url in urls]

    def parse_product_page(self, response):
        items = SnkrsItem()

        if self.get_retailer_sku(response) in self.product_id:
            pass

        self.product_id.add(self.get_retailer_sku(response))
        items['retailer_sku'] = self.get_retailer_sku(response)
        items['brand'] = self.get_brand(response)
        items['category'] = self.get_category(response)
        items['description'] = self.get_desciption(response)
        items['gender'] = self.get_gender(response)
        items['url'] = response.url
        items['name'] = self.get_name(response)
        items['image_urls'] = self.get_image_urls(response)
        items['skus'] = self.get_skus(items, response)

        yield items

    def get_retailer_sku(self, response):
        return response.css('.nosto_product .product_id::text').getall()[0]

    def get_brand(self, response):
        return response.css('.nosto_product .brand::text').getall()[0]

    def get_category(self, response):
        return response.css('.nosto_category::text').getall()[0]

    def get_desciption(self, response):
        description = '//p[@id="product_reference"]/label/text() | //div[@id="short_description_content"]/p/text()'

        return response.xpath(description).getall()

    def get_gender(self, response):
        gender = response.css('.nosto_category::text').re_first(r'(Men|Women)')

        return "men" if gender == "Men" else "women" if gender == "Women" else "unisex-adults"

    def get_name(self, response):
        return response.css('.nosto_product .name::text').getall()[0]

    def get_image_urls(self, response):
        return response.css('.image_url::text, .alternate_image_url::text').getall()

    def get_skus(self, items, response):
        colour = re.sub(r'.*- ', '', items['name'])
        skus = {}

        for sizes in response.css('span.units_container .size_EU::text').getall():

            skus[colour + "_" + sizes] = {
                "colour": colour,
                "currency": response.css('.nosto_product .price_currency_code::text').getall()[0],
                "original_price": float(response.css('div.nosto_product .price::text').getall()[0]),
                "size": sizes,
            }

            if response.xpath('//span[@id="reduction_percent_display"]/text()').getall():

                skus["previous_price"] = float(response.css('.nosto_product .list_price::text').getall()[0]) 

            skus.update(skus)

        return skus
