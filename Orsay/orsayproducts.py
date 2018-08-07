# -*- coding: utf-8 -*-
import scrapy
import json
import re


class OrsayproductSpider(scrapy.Spider):
    name = 'orsayproducts'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']

    def parse(self, response):
        product_url = self.get_product_page(response)
        yield scrapy.Request(
            url=product_url, callback=self.parse_categories)

    def parse_categories(self, response):
        categories_urls = self.get_categories(response)
        for url in categories_urls:
            yield scrapy.Request(
                url=url+"?sz=72", callback=self.parse_listings)

    def parse_listings(self, response):
        product_detials_urls = self.get_product_details_urls(response)
        next_page = self.get_next_page(response)
        if next_page:
            yield scrapy.Request(
                    url=next_url, callback=self.parse_listings)
        for url in product_detials_urls:
            yield scrapy.Request(
                    url=url, callback=self.parse_product)

    def parse_product(self, response):
        product_imgs = self.get_product_imgs(response)
        product_details = self.get_product_details(response)
        colors = self.get_product_colors(response)
        sizes = self.get_product_sizes(response)
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
        description = self.clean_text(description)
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

    def clean_text(self, text):
        text = [txt.strip() for txt in text]
        return list(filter(lambda txt: txt != '', text))
    
    def get_number(self, text_str):
        return re.findall(r'\d+', text_str)[0]

    def get_product_page(self, response):
        product_urls = response.css(".level-1 a::attr(href)").extract()
        return ([url for url in product_urls if "produkte" in url])[0]
    
    def get_categories(self, response):
        return response.css(
                ".refinement-category-item a::attr(href)").extract()
    
    def get_product_details_urls(self, response):
        product_detials_urls = response.css(
                ".grid-tile .product-image a::attr(href)").extract()
        return [response.urljoin(url)
                for url in product_detials_urls]
    
    def get_total_products(self, response):
        total_products = response.css(
                ".load-more-progress-label::text").extract()[1]
        return self.get_number(total_products)
    
    def get_next_page(self, response):
        total_products = self.get_total_products(response)
        listed_products = self.get_number(response.url)
        if int(total_products) < int(listed_products):
            return response.url.replace(
                    listed_products, str(int(listed_products)+72))
        else:
            return None

    def get_product_imgs(self, response):
        product_imgs = response.css(".productthumbnail::attr(src)").extract()
        return ([img.replace("sw=100", "sw=700").replace(
                "sh=150", "sh=750") for img in product_imgs])

    def get_product_details(self, response):
        details = response.css(".js-product-content-gtm").extract_first()
        product_data = details[details.find("{"):(details.find("}")+1)]
        return json.loads(product_data)

    def get_product_colors(self, response):
        colors = response.css(".swatches img::attr(alt)").extract()
        return [color[color.find("- ")+2:] for color in colors]
    
    def get_product_sizes(self, response):
        sizes = response.css(".swatches a::text").extract()
        return [size.replace("\n", "") for size in sizes if size is not "\n"]