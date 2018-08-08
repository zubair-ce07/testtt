import scrapy
from urllib.parse import urljoin


class Parser(scrapy.Spider):
    name = "Parser"
    product = {}
    response = None
    possible_genders = {"men", "women", "girls", "boys"}
    Default_gender = "unisex_adults"

    def parse(self, response):
        if response.css('body.pda'):
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
            yield self.product
            yield from self.colour_requests()
        else:
            self.logger.error('skipping %s because of multiple products page layout.', response.url)

    def get_skus(self):
        common_sku = {
            "price": self.get_price(),
            "currency": self.get_currency(),
            "colour": self.get_colour()
        }
        raw_skus = self.response.css('option[data-code]')
        skus = {}
        for raw_sku in raw_skus:
            sku = common_sku.copy()
            if raw_sku.css('[class*="unavailable"]'):
                sku["out_of_stock"] = True
            if self.previous_prices(raw_sku):
                sku["previous_prices"] = self.previous_prices(raw_sku)
            skus[raw_sku.css("::attr(data-code)").extract_first()] = sku
        return skus

    def get_price(self):
        price = self.response.css('meta[itemprop="price"]::attr(content)').extract_first()
        return 100 * float(price.replace(',', '.'))

    def get_currency(self):
        return self.response.css('meta[itemprop="currency"]::attr(content)').extract_first()

    def get_colour(self):
        return self.get_name().split("in ")[-1]

    def get_name(self):
        return self.response.css('h2[itemprop="name"]::text').extract_first()

    def get_gender(self):
        category = self.get_category()
        return category[0].lower() if category[0].lower() in self.possible_genders else self.Default_gender

    def get_category(self):
        return self.response.css('#breadcrumb a::text').extract()

    def get_image_urls(self):
        image_paths = self.response.css('li[data-mimetype="image/jpeg"]::attr(data-detail)').extract()
        return [urljoin(self.response.url, path) for path in image_paths]

    def get_retailer_sku(self):
        return self.response.css('span[data-code]::attr(data-code)').extract_first()

    @staticmethod
    def previous_prices(option):
        previous_price = option.css("::attr(data-listprice)").extract_first()
        return [100 * float(previous_price[:-2].replace(",", "."))] if previous_price else []

    def get_description(self):
        return self.response.css('div[itemprop=description]>div:nth-child(2) ::text').extract()

    def get_care(self):
        care_lines = self.response.css('div[itemprop=description]>div:last-child').css(' ::text').extract()
        care_lines = [line.strip() for line in care_lines]
        care_lines = ''.join(care_lines)
        return care_lines.split(". ")

    def colour_requests(self):
        colour_urls = self.response.css('.colors a::attr(href)').extract()
        trail = self.response.meta.get("trail", []).copy()
        trail.append(self.response.url)
        for url in colour_urls:
            request = self.response.follow(url, callback=self.parse)
            request.meta["trail"] = trail
            yield request

    def is_outofstock(self):
        return self.response.css('meta[itemprop="availability"][content="out_of_stock"]')
