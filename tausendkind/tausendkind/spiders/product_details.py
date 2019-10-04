"""
Product details module.

This module outputs a json format file
for the website's product details.
"""
import re

import scrapy


def get_sku(response):
    """Return product's sku."""
    return re.findall(r'"sku":\"(.*?)\"', response.css(
        "#catalog-product-view > script:nth-child(2)::text").get())[0]


def get_product_name(response):
    """Return product's name."""
    return response.css("#product-name::text").get()


def get_description(response):
    """Return product's description."""
    return response.css("div.pdp-description-container div:nth-child(2) p::text").get().strip()


def get_price(response):
    """Return product's price."""
    return re.findall(r"\d+,\d+", response.css("strong.pdp-price::text").get())[0]


def get_original_price(response):
    """Return product's original price if discounted."""
    return re.findall(r"\d+,\d+", response.css("del.pdp-reduction strong::text").get())[0]


def get_currency(response):
    """Return product's currency."""
    return re.findall(r"[A-Z]{3}", response.css("strong.pdp-price::text").get())[0]


def get_variant_sizes(response):
    """Return product's variant sizes in a list."""
    variant_sizes = response.css("li.select__option::attr(data-sizeval)").extract()
    return variant_sizes if not variant_sizes == '[]' else ''


def get_variant_sizes_out_of_stock(response):
    """Return product's sizes out of stock in a list."""
    sizes_out_of_stock = response.css(
        "li.select__option.disabled::attr(data-sizeval)").extract()
    return sizes_out_of_stock if not sizes_out_of_stock == '[]' else ''


class ProductDetailsSpider(scrapy.Spider):
    """
    Product Details Spider Class.

    This class initializes a spider and has
    all the required methods to display
    each product's details.
    """

    name = "product_details"
    start_urls = ["https://www.tausendkind.de/"]

    def parse(self, response):
        """
        Parse for Header Urls.

        This function returns the header bar
        urls and yields a scrapy request for each.
        """
        for header_url in response.css("ul.flex-items-lg-between > li > a::attr(href)").extract():
            yield scrapy.Request(url=header_url, callback=self.parse_urls)

    def parse_urls(self, response):
        """
        Parse for sub urls.

        This function returns the sub
        urls from each header url and yields a
        scrapy request for each.
        """
        sub_urls = response.css("ul.filters li.l2 a::attr(href)").extract()
        if "magazin/inspiration" not in response.url:
            if "concept-store" not in response.url:
                sub_urls.append(response.url)
            for sub_url in sub_urls:
                yield scrapy.Request(url=sub_url, callback=self.parse_product_urls)

    def parse_product_urls(self, response):
        """
        Parse for product urls.

        This function returns the product
        urls from each sub url and yields a
        scrapy request for each.
        """
        for url_key in re.findall(
                r'"url_key":\"(.*?)\"',
                response.css("#main > div.row.rel.old-row > script:nth-child(6)::text").get()):
            yield scrapy.Request(
                url="https://www.tausendkind.de/{}".format(url_key),
                callback=self.parse_details)

    @staticmethod
    def parse_details(response):
        """
        Parse for product details.

        This function yields the product
        details for each product url. Details
        include Sku, Name, description, price,
        currency, sizes and sizes out of stock.
        """
        price = get_price(response)
        original_price = get_original_price(response)
        yield {
            "Sku": get_sku(response),
            "product_name": get_product_name(response),
            "description": get_description(response),
            "price": price,
            "original_price": original_price if not price == original_price else "",
            "currency": get_currency(response),
            "variant_sizes": get_variant_sizes(response),
            "variant_sizes_out_of_stock": get_variant_sizes_out_of_stock(response),
        }
