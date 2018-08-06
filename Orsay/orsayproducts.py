# -*- coding: utf-8 -*-
import scrapy
import json


class OrsayproductSpider(scrapy.Spider):
    name = 'orsayproducts'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']

    def parse(self, response):
        product_urls = response.css(".level-1 a::attr(href)").extract()
        product_url = [url for url in product_urls if "produkte" in url]
        yield scrapy.Request(
            url=product_url[0], callback=self.parse_categories)

    def parse_categories(self, response):
        categories_links = response.css(
            ".refinement-category-item a::attr(href)").extract()
        for link in categories_links:
            if response.request.url in categories_links:
                yield scrapy.Request(
                    url=link, callback=self.parse_listings)
            else:
                yield scrapy.Request(
                    url=link, callback=self.parse_categories)

    def parse_listings(self, response):
        product_detials_urls = response.css(
            ".grid-tile .product-image a::attr(href)").extract()
        product_detials_urls = [response.urljoin(url)
                                for url in product_detials_urls]
        for link in product_detials_urls:
            yield scrapy.Request(
                    url=link, callback=self.parse_product)
        # handle pagination here

    def parse_product(self, response):
        product_imgs = response.css(".productthumbnail::attr(src)").extract()
        product_imgs = ([img.replace("sw=100", "sw=700").replace(
            "sh=150", "sh=750") for img in product_imgs])
        details = response.css(".js-product-content-gtm").extract_first()
        product_data = details[details.find("{"):(details.find("}")+1)]
        product_details = json.loads(product_data)
        colors = response.css(".swatches img::attr(alt)").extract()
        colors = [color[color.find("- ")+2:] for color in colors]
        sizes = response.css(".swatches a::text").extract()
        sizes = [size.replace("\n", "") for size in sizes if size is not "\n"]
        product_skus = {}
        for size in sizes:
            for color in colors:
                product_skus = {
                    product_details["productId"]+"_"+size: {
                        "color": product_details["color"],
                        "currency": product_details["currency_code"],
                        "price": product_details["netPrice"],
                        "size": product_details["size"]
                    }
                }
        description = response.css(".product-details div::text").extract()
        description = self.clean_input(description)
        yield {
            "brand": "Orsay",
            "description": description,
            "product_imgs": product_imgs,
            "category": product_details["categoryName"],
            "name": product_details["name"],
            "skus": product_skus,
            "url": response.request.url
            # hande care for product too
        }

        def clean_input(self, input):
            input = [desc.strip() for desc in input]
            input = list(filter(lambda desc: desc != '', input))
            return input
