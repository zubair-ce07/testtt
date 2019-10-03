"""
Product details module.

This module outputs a json format file
for the website's product details.
"""
import re
from datetime import datetime
import scrapy


class ProductDetailsSpider(scrapy.Spider):
    """
    Product Details Spider Class.

    This class initializes a spider and has
    all the required methods to display
    each product's details.
    """

    name = "product_details"
    start_urls = ["https://www.tausendkind.de/"]

    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,
        "FEED_FORMAT": "json",
        "FEED_URI": "{}_{}.json".format(name, datetime.now()),
    }

    def parse(self, response):
        """
        Parse for Header Urls.

        This function returns the header bar
        urls and yields a scrapy request for each.
        """
        for header_url in response.css(
                "ul.flex-items-lg-between > li > a::attr(href)"
        ).extract():
            yield scrapy.Request(url=header_url,
                                 callback=self.parse_urls)

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
                yield scrapy.Request(url=sub_url,
                                     callback=self.parse_product_urls)

    def parse_product_urls(self, response):
        """
        Parse for product urls.

        This function returns the product
        urls from each sub url and yields a
        scrapy request for each.
        """
        for url_key in re.findall(
                r'"url_key":\"(.*?)\"',
                response.css(
                    "#main > div.row.rel.old-row > script:nth-child(6)::text"
                    ).get()):
            yield scrapy.Request(
                url="https://www.tausendkind.de/{}".format(url_key),
                callback=self.parse_details,
            )

    @staticmethod
    def parse_details(response):
        """
        Parse for product details.

        This function yields the product
        details for each product url. Details
        include Sku, Name, description, price,
        currency, sizes and sizes out of stock.
        """
        description = (
            response.css(
                "div.pdp-description-container div div:nth-child(2)::text")
            .get().replace("\n", "").replace("\r", "").replace("  ", "")
        )
        description = (
            response.css(
                "div.pdp-description-container div:nth-child(2) p::text")
            .get().replace("\n", "").replace("\r", "").replace("  ", "")
            if not description else description
        )
        price = response.css("strong.pdp-price::text").re_first(r"\d+,\d+")
        original_price = response.css(
            "del.pdp-reduction strong::text").re_first(
                r"\d+,\d+")
        yield {
            "Sku": response.css(
                "#catalog-product-view > script:nth-child(2)").re_first(
                    r'"sku":\"(.*?)\"'),
            "product_name": response.css("#product-name::text").get(),
            "description": description,
            "price": price,
            "original_price": original_price
                              if not price == original_price else "",
            "currency": response.css("strong.pdp-price::text")
                        .re_first(r"[A-Z]{3}"),
            "variant_sizes": response.css(
                "li.select__option::attr(data-sizeval)"
            ).extract(),
            "variant_sizes_out_of_stock": response.css(
                "li.select__option.disabled::attr(data-sizeval)"
            ).extract(),
        }
