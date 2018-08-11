import json

import scrapy
from w3lib.url import url_query_cleaner as w3cleaner


class Parser(scrapy.Spider):
    name = "parser"
    possible_genders = {"men", "women", "girls", "boys"}
    default_gender = "unisex_adults"
    scraped_ids = []

    def parse(self, response):
        product = {}
        product_data = self.get_product_json(response)
        if product_data.get("id") in self.scraped_ids:
            return
        else:
            self.scraped_ids.append(product_data.get("id"))
        product["retailer_sku"] = product_data.get("id")
        product["name"] = product_data.get("name") if product_data.get("name") else ""
        product["image_urls"] = []
        product["lang"] = "en"
        product["gender"] = product_data.get("gender")
        product["category"] = self.get_categories(response)
        product["industry"] = None
        product["brand"] = product_data.get("brand")
        product["url"] = response.url
        product["market"] = "US"
        product["trail"] = response.meta.get("trail", []).copy()
        product["retailer"] = "hugoboss"
        product["url_original"] = response.url
        product["description"] = self.get_description(response)
        product["care"] = self.get_care(response)
        product["skus"] = {}
        response.meta["pending_color_reqs"] = self.colour_requests(response)
        response.meta["product"] = product
        return self.get_skus(response)

    def get_skus(self, response):
        product = response.meta["product"].copy()
        product["image_urls"].extend(self.get_image_urls(response))
        common_sku = {}
        product_data = self.get_product_json(response)
        common_sku["price"] = product_data.get("price")
        common_sku["currency"] = self.get_currency(response)
        common_sku["colour"] = self.get_colour(response)
        sku_variant = product_data.get("variant")
        sizes = response.css('.swatch-list__size::text').extract()
        if not sizes:
            sizes.append("One Size")
        unavailable_sizes = response.css('.swatch-list__size[class*="unselectable"]::text').extract()
        for size in sizes:
            sku = common_sku.copy()
            sku["size"] = size.strip()
            if size in unavailable_sizes:
                sku["out_of_stock"] = True
            if product_data.get("metric3"):
                sku["previous_prices"] = [product_data.get("price") + product_data.get("metric3")]
            product["skus"][f"{sku_variant}_{size}"] = sku
        if not response.meta["pending_color_reqs"]:
            return product
        next_color_req = response.meta["pending_color_reqs"].pop()
        next_color_req.meta["product"] = product
        next_color_req.meta["pending_color_reqs"] = response.meta["pending_color_reqs"].copy()
        return next_color_req

    @staticmethod
    def get_currency(response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    @staticmethod
    def get_colour(response):
        variation_json = response.css('.product-variations::attr(data-current)').extract_first()
        json_object = json.loads(variation_json)
        return json_object.get("color").get("displayValue")

    @staticmethod
    def get_categories(response):
        unique_breadcrumbs = set(response.css('.breadcrumb__link::attr(title)').extract())
        unique_breadcrumbs.remove("Home")
        unique_breadcrumbs.remove("Shop")
        return list(unique_breadcrumbs)

    @staticmethod
    def get_image_urls(response):
        image_paths = response.css('img.slider-item__image::attr(src)').extract()
        return [w3cleaner(path) for path in image_paths]

    @staticmethod
    def get_description(response):
        paragraph = response.css('div.product-container__text__description::text').extract_first()
        return paragraph.strip().split('.\n\n') if paragraph else []

    @staticmethod
    def get_care(response):
        material_care = response.css('.materialCare>.product-container__text::text').extract_first()
        material_care = material_care.strip().split(", ") if material_care else []
        care = response.css('.accordion__care-icon__text::text').extract()
        material_care.extend(care if care else [])
        return material_care

    @staticmethod
    def get_product_json(response):
        json_string = response.css('div[data-as-product]::attr(data-as-product)').extract_first()
        json_string.replace('&quot;', '"')
        return json.loads(json_string)

    def colour_requests(self, response):
        colour_urls = response.css('.swatch-list__image::attr(href)').extract()
        colour_requests = []
        for url in colour_urls:
            request = response.follow(w3cleaner(url), self.get_skus)
            if response.url != request.url:
                colour_requests.append(request)
        return colour_requests
