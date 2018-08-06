import scrapy
from urllib.parse import urlparse
import w3lib.url as w3url


class Parser(scrapy.Spider):
    name = "Parser"
    common_sku = {}
    product = {}
    response = None
    possible_genders = {"Men", "Women", "Girls", "Boys"}
    Default_gender = "Unisex_Adults"

    def parse(self, response):
        self.response = response
        self.product["retailer_sku"] = self.get_retailer_sku()
        self.product["lang"] = "de"
        self.product["gender"] = self.get_gender()
        self.product["category"] = self.get_category()
        self.product["industry"] = None
        self.product["brand"] = "Joop"
        self.product["url"] = w3url.url_query_cleaner(response.url)
        self.product["market"] = "DE"
        self.product["retailer"] = "joop-de"
        self.product["url_original"] = response.url
        self.product["name"] = self.get_name()
        self.product["description"] = self.get_description()
        self.product["care"] = self.get_care()
        self.product["image_urls"] = self.get_image_urls()
        self.product["skus"] = self.get_skus()
        self.product["price"] = self.get_price()
        self.product["currency"] = self.get_currency()
        return self.product

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

    def get_price(self):
        price = self.response.css('meta[itemprop="price"]::attr(content)').extract_first()
        return 100 * float(price.replace(',', '.'))

    def get_currency(self):
        return self.response.css('meta[itemprop="currency"]::attr(content)').extract_first()

    def get_colour(self):
        return self.get_name().split()[-1]

    def get_name(self):
        return self.response.css('h2[itemprop="name"]::text').extract_first()

    def get_gender(self):
        category = self.get_category()
        return category[0] if category[0] in self.possible_genders else self.Default_gender

    def get_category(self):
        return self.response.css('#breadcrumb a::text').extract()

    def get_image_urls(self):
        image_paths = self.response.css('li[data-mimetype="image/jpeg"]::attr(data-detail)').extract()
        url = urlparse(self.response.url)
        return [f'{url.scheme}://{url.netloc}{path}' for path in image_paths]

    def get_retailer_sku(self):
        return self.response.css('span[data-code]::attr(data-code)').extract_first()

    @staticmethod
    def previous_prices(option):
        previous_price = option.css("::attr(data-listprice)").extract_first()
        return [100 * float(previous_price[:-2].replace(",", "."))]

    def get_description(self):
        return self.response.css('div[itemprop=description]>div>p::text').extract_first().split(". ")

    def get_care(self):
        care_lines = self.response.css('div[itemprop=description]>div:last-child').css(' ::text').extract()
        care_lines = [line.strip() for line in care_lines]
        care_lines = ''.join(care_lines)
        return care_lines.split(". ")
