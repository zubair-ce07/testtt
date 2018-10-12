# -*- coding: utf-8 -*-
import re
import json
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from shopjusticebot.items import ShopjusticeProduct


class ShopjusticeSpider(CrawlSpider):
    name = 'shopjustice'
    allowed_domains = ['shopjustice.com']
    start_urls = ['http://www.shopjustice.com']

    rules = (
        Rule(
            LinkExtractor(
                allow=(r'.*/P-\d+')
            )
        ),
        Rule
        (
            LinkExtractor(
                allow=(r'.*/prd-\d+')
            ),
            callback='parse_product_details'
        )

    )

    def parse_product_details(self, response):
        product = ShopjusticeProduct()

        product["product_id"] = response.css(
            "#pdpProductID::attr(value)"
            ).extract_first()

        product["brand"] = "Shopjustice"
        product["name"] = response.css(
            ".jst-product-title::text"
            ).extract_first()

        product["url"] = response.url
        product["category"] = self.get_category(response)
        description = response.css("#tab1")
        if description:
            product["description"] = description[0].css("li::text").extract()
        product["care"] = response.css(
            "#tab2 li:nth-child(1)::text"
            ).extract_first()
        product["image_urls"] = self.get_img_urls(
            response, product["product_id"]
            )
        product["skus"] = {}
        product["skus"] = self.get_skus_detail(response)

        yield product

    def get_img_urls(self, response, pid):
        # Image issue check url
        colour_code = self.get_colours(response, "ids")
        img_urls = []
        img_start_link = "https://shopjustice.scene7.com/is/" \
            + "image/justiceProdATG/"

        img_end_link = "?fmt=jpeg&qlt=95,0&resMode=sharp2&op_usm=0.8,1.0,8,0" \
            + "&op_sharpen=1&fit=constrain,1&wid=478&hei=690"
        diff_img = ["", "_alt1", "_atl2", "_Back"]
        for colour in colour_code:
            for dif in diff_img:
                url = img_start_link + pid + "_" + colour + dif + img_end_link
                img_urls.append(url)

        return img_urls

    def get_category(self, response):
        json_data = self.get_json_data(response)
        ensighten_data = json_data["pdpDetail"]["product"][0]
        ensighten_data = ensighten_data["ensightenData"][0]

        category = ensighten_data["categoryPath"]

        return category

    def get_colours(self, response, key):
        json_data = self.get_json_data(response)

        available_colour = json_data["pdpDetail"]["product"][0]
        available_colour = available_colour["all_available_colors"]
        available_colour = available_colour[0]["values"]

        colours = []

        for colour in available_colour:
            if key is "name":
                colours.append(colour["name"])

            elif key is "ids":
                colours.append(colour["id"])

        return colours

    def get_sizes(self, response):
        json_data = self.get_json_data(response)
        sizes = []
        available_sizes = json_data["pdpDetail"]["product"][0]
        available_sizes = available_sizes["all_available_sizes"][0]["values"]

        for size in available_sizes:
            sizes.append(size["value"])

        return sizes

    def get_json_data(self, response):
        json_str = response.css("#pdpInitialData::text").extract_first()
        json_data = json.loads(json_str)

        return json_data

    def get_skus_detail(self, response):
        colours = self.get_colours(response, "name")
        sizes = self.get_sizes(response)
        prices = self.get_product_prices(response)
        skus = {}

        currency = ''
        if prices:
            currency = re.search(r'([^0-9.])', prices[0]).group(1)
            prices[0] = float(re.search(r'(\d+\.\d+)', prices[0]).group(1))
            prices[1] = float(re.search(r'(\d+\.\d+)', prices[1]).group(1))

        for colour in colours:
            for size in sizes:
                skus[colour + '_' + size] = {
                    "colour": colour,
                    "currency": currency,
                    "previouse_price": prices[0],
                    "price": prices[1],
                    "size": size,
                }
        return skus

    def get_product_prices(self, response):
        json_data = self.get_json_data(response)
        prices = []

        values = json_data["pdpDetail"]["product"][0]
        values = values["all_available_colors"][0]["values"]

        previous_price = values[0]["prices"]["list_price"]
        price = values[0]["prices"]["sale_price"]

        prices.append(previous_price)
        prices.append(price)

        return prices
