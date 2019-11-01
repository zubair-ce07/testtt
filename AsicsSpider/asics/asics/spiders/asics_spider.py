import scrapy
from scrapy.http.request import Request
import re
from asics.items import AsicsItem
from datetime import datetime


class AsicsSpider(scrapy.Spider):
    name = 'asics'
    allowed_domains = ["asics.com"]
    product = AsicsItem()
    product_variant_links = []

    def start_requests(self):
        yield Request(url="http://www.asics.com/us/en-us/", callback=self.parse_categories)

    def parse_categories(self, response):
        for link in response.css(".show-menu-item::attr(href)").getall():
            yield response.follow(link, callback=self.parse_products)  # going to one layer deep from landing page

    def parse_products(self, response):
        products = response.css(".product-image a::attr(href)").getall()
        next_page = response.css(".page-next::attr(href)").get()
        for link in products:
            yield response.follow(link, callback=self.parse_single_product)
        if next_page:
            yield response.follow(next_page, callback=self.parse_products)

    def parse_single_product(self, response):
        self.product['description'] = description(response)
        self.product['product_name'] = product_name(response)
        self.product['category'] = product_category(response)
        self.product['image_urls'] = []
        self.product['skus'] = {}
        self.product['date'] = datetime.now().timestamp()
        self.product['price'] = price(response)
        self.product['url'] = response.url
        self.product['original_url'] = response.url

        script = response.xpath('//script[@type="text/javascript"]')
        self.product['brand'] = brand(script)
        self.product['currency'] = currency(script)
        self.product['lang'] = lang(script)
        self.product['gender'] = gender(script)

        self.product_variants_links = response.css(".js-color::attr(href)").getall()[1:]
        for product in self.parse(response):
            if not isinstance(product, Request):
                yield product

    def parse(self, response):
        self.product['image_urls'] += image_urls(response)
        self.product['skus'].update(parse_sku(response))

        if len(self.product_variant_links) > 0:
            page = self.product_variant_links[0]
            del self.product_variant_links[0]
            yield response.follow(page, callback=self.parse)
        else:
            yield self.product


def product_name(response):
    return response.css(".pdp-top__product-name::text").get().strip()


def product_category(response):
    return [response.css(".product-classification span::text").get()]


def description(response):
    return response.css(".product-info-section-inner::text").get().strip()


def image_urls(response):
    images = response.css(".thumbnail-link::attr(href)").getall()
    if '#' in images:
        images.remove('#')
    return images


def product_category(response):
    return [response.css(".product-classification span::text").get()]


def price(response):
    return response.css(".price-sales::text").extract()[1].strip()[1:]


def brand(script):
    return script.re(r'"brand": "(\w+)"')


def currency(script):
    return script.re(r'"currency": "(\w+)"')


def lang(script):
    return script.re(r'"language": "(\w+)"')


def gender(script):
    return script.re(r'"product_gender": \[\n +"(\w+)"')


def sku(response):
    return response.css(".product-number span+ span::text").get().strip()


def colour(response):
    return response.css(".variants__header--light::text").get().strip()


def sku_sizes(response):
    return response.css(".variation-group-value .js-ajax::text").getall()


def parse_sku(response):
    skus = {}
    product_sku = sku(response)
    product_colour = colour(response)
    product_sku_sizes = sku_sizes(response)

    for sku_size in product_sku_sizes:
        sku_size = sku_size.strip()
        skus[f"{product_sku.replace('.', '|')}|{product_colour}|{sku_size}"] = {
            "colour": product_colour,
            "size": sku_size,
            "price": price(response),
            'currency': 'USD'
        }

    return skus
