import json

import scrapy
import w3lib.url as w3url


class Parser(scrapy.Spider):
    name = "Parser"
    possible_genders = {"men", "women", "girls", "boys"}
    default_gender = "unisex_adults"

    def parse(self, response):
        product = {}
        product["retailer_sku"] = self.get_retailer_sku(response)
        product["lang"] = "de"
        product["gender"] = self.get_gender(response)
        product["category"] = self.get_categories(response)
        product["industry"] = None
        product["brand"] = self.get_brand(response)
        product["url"] = response.url
        product["market"] = "DE"
        product["trail"] = response.meta["trail"].copy()
        product["retailer"] = "joop-de"
        product["url_original"] = response.url
        product["name"] = self.get_name(response)
        product["description"] = self.get_description(response)
        product["care"] = self.get_care(response)
        product["image_urls"] = self.get_image_urls(response)
        product["skus"] = self.get_skus(response)
        product["price"] = self.get_price(response)
        product["currency"] = self.get_currency(response)
        yield product
        yield from self.colour_requests(response)

    def get_skus(self, response):
        common_sku = {}
        common_sku["price"] = self.get_price(response)
        common_sku["currency"] = self.get_currency(response)
        common_sku["colour"] = self.get_colour(response)
        sku_id_prefix = self.get_retailer_sku(response)
        skus = {}
        sizes = response.css('.swatch-list__size::text').extract()
        unavailable_sizes = response.css('.swatch-list__size[class*="unselectable"]::text').extract()
        for size in sizes:
            sku = common_sku.copy()
            sku["size"] = size.strip()
            if size in unavailable_sizes:
                sku["out_of_stock"] = True
            skus[f"{sku_id_prefix}_{size.strip()}"] = sku
        return skus

    @staticmethod
    def get_price(response):
        return float(response.css('meta[itemprop="price"]::attr(content)').extract_first())

    @staticmethod
    def get_currency(response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    @staticmethod
    def get_colour(response):
        variation_json = response.css('.product-variations::attr(data-current)').extract_first()
        json_object = json.loads(variation_json)
        return json_object.get("color").get("displayValue")

    @staticmethod
    def get_name(response):
        return response.css('h1[itemprop="name"]::text').extract_first()

    def get_gender(self, response):
        categories = self.get_categories(response)
        for category in categories:
            if category.lower() in self.possible_genders:
                return category.lower()
        return self.default_gender

    @staticmethod
    def get_categories(response):
        unique_breadcrumbs = set(response.css('.breadcrumb__link::attr(title)').extract())
        unique_breadcrumbs.remove("Home")
        unique_breadcrumbs.remove("Shop")
        return list(unique_breadcrumbs)

    @staticmethod
    def get_image_urls(response):
        image_paths = response.css('img.slider-item__image::attr(src)').extract()
        return [w3url.url_query_cleaner(path) for path in image_paths]

    @staticmethod
    def get_retailer_sku(response):
        return response.css('div[data-variationgroupid]::attr(data-variationgroupid)').extract_first()

    @staticmethod
    def get_description(response):
        return response.css('div.product-container__text__description::text').extract_first().strip().split('.\n\n')

    @staticmethod
    def get_care(response):
        return response.css('.accordion__care-icon__text::text').extract()

    def colour_requests(self, response):
        colour_urls = response.css('.swatch-list__image::attr(href)').extract()
        trail = response.meta.get("trail", [])
        for url in colour_urls:
            request = response.follow(url, callback=self.parse)
            request.meta["trail"] = trail.copy().append(response.url)
            yield request

    def get_brand(self, response):
        pass
