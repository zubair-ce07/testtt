import json
import scrapy
from urllib.parse import urlparse
import w3lib.url as w3url


class Parser(scrapy.Spider):
    name = "Parser"
    common_sku = {}
    product = {}
    response = None
    possible_genders = {"men", "women", "girls", "boys"}
    Default_gender = "unisex_adults"

    def parse(self, response):
        self.response = response
        self.product["retailer_sku"] = self.get_retailer_sku()
        self.product["lang"] = "de"
        self.product["gender"] = self.get_gender()
        self.product["category"] = self.get_category()
        self.product["industry"] = None
        self.product["brand"] = "Joop"
        self.product["url"] = self.response.url
        self.product["market"] = "DE"
        self.product["trail"] = self.response.meta["trail"].copy()
        self.product["retailer"] = "joop-de"
        self.product["url_original"] = self.response.url
        self.product["name"] = self.get_name()
        self.product["description"] = self.get_description()
        self.product["care"] = self.get_care()
        self.product["image_urls"] = self.get_image_urls()
        if not self.is_outofstock():
            self.product["skus"] = self.get_skus()
            self.product["price"] = self.get_price()
            self.product["currency"] = self.get_currency()
        else:
            self.product["out_of_stock"] = True
        product_or_url = [self.product]
        product_or_url.extend(self.colour_urls())
        return product_or_url

    def get_skus(self):
        self.common_sku["price"] = self.get_price()
        self.common_sku["currency"] = self.get_currency()
        self.common_sku["colour"] = self.get_colour()
        options = self.response.css('option[data-code]')
        skus = {}
        for option in options:
            sku = self.common_sku.copy()
            if "unavailable" in option.css("::attr(class)").extract_first().split():
                sku["out_of_stock"] = True
            if self.previous_prices(option):
                sku["previous_prices"] = self.previous_prices(option)
            skus[option.css("::attr(data-code)").extract_first()] = sku
        return skus

    #done
    def get_price(self):
        return float(self.response.css('meta[itemprop="price"]::attr(content)').extract_first())

    #done
    def get_currency(self):
        return self.response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    #done
    def get_colour(self):
        variation_json = self.response.css('.product-variations::attr(data-current)').extract_first()
        json_object = json.loads(variation_json)
        return json_object.get("color").get("displayValue")

    #done
    def get_name(self):
        return self.response.css('h1[itemprop="name"]::text').extract_first()

    def get_gender(self):
        category = self.get_category()
        return category[0] if category[0] in self.possible_genders else self.Default_gender

    def get_category(self):
        return self.response.css('.breadcrumb__title::text').extract()

    #done
    def get_image_urls(self):
        image_paths = self.response.css('img.slider-item__image::attr(src)').extract()
        return [w3url.url_query_cleaner(path) for path in image_paths]

    #done
    def get_retailer_sku(self):
        return self.response.css('div[data-variationgroupid]::attr(data-variationgroupid)').extract_first()

    @staticmethod
    def previous_prices(option):
        previous_price = option.css("::attr(data-listprice)").extract_first()
        return [100 * float(previous_price[:-2].replace(",", "."))] if previous_price else []

    #done
    def get_description(self):
        return self.response.css('div.product-container__text__description::text').extract_first().strip().split('.\n\n')

    #done
    def get_care(self):
        return self.response.css('.accordion__care-icon__text::text').extract()

    def colour_urls(self):
        return self.response.css('.colors a::attr(href)').extract()

    def is_outofstock(self):
        return False
