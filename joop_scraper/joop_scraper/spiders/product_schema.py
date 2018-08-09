from urllib.parse import urljoin

import scrapy


class Parser(scrapy.Spider):
    name = "Parser"
    possible_genders = {"men", "women", "girls", "boys"}
    default_gender = "unisex_adults"

    def parse(self, response):
        product = {}
        if response.css('body.pda'):
            self.logger.error('skipping %s because of multiple products page layout.', response.url)
            return
        product["retailer_sku"] = self.get_retailer_sku(response)
        product["lang"] = "de"
        product["gender"] = self.get_gender(response)
        product["category"] = self.get_category(response)
        product["industry"] = None
        product["brand"] = "Joop"
        product["url"] = response.url
        product["market"] = "DE"
        product["trail"] = response.meta["trail"].copy()
        product["retailer"] = "joop-de"
        product["url_original"] = response.url
        product["name"] = self.get_name(response)
        product["description"] = self.get_description(response)
        product["care"] = self.get_care(response)
        product["image_urls"] = self.get_image_urls(response)
        if not self.is_outofstock(response):
            product["skus"] = self.get_skus(response)
            product["price"] = self.get_price(response)
            product["currency"] = self.get_currency(response)
        else:
            product["out_of_stock"] = True
        yield product
        yield from self.colour_requests(response)

    def get_skus(self, response):
        common_sku = {
            "price": self.get_price(response),
            "currency": self.get_currency(response),
            "colour": self.get_colour(response)
        }
        raw_skus = response.css('option[data-code]')
        skus = {}
        for raw_sku in raw_skus:
            sku = common_sku.copy()
            if raw_sku.css('[class*="unavailable"]'):
                sku["out_of_stock"] = True
            if self.previous_prices(raw_sku):
                sku["previous_prices"] = self.previous_prices(raw_sku)
            skus[raw_sku.css("::attr(data-code)").extract_first()] = sku
        return skus

    def get_colour(self, response):
        return self.get_name(response).split("in ")[-1]

    @staticmethod
    def get_name(response):
        return response.css('h2[itemprop="name"]::text').extract_first()

    def get_gender(self, response):
        category = self.get_category(response)
        return category[0].lower() if category[0].lower() in self.possible_genders else self.default_gender

    @staticmethod
    def previous_prices(raw_sku):
        previous_price = raw_sku.css("::attr(data-listprice)").extract_first()
        return [100 * float(previous_price[:-2].replace(",", "."))] if previous_price else []

    @staticmethod
    def is_outofstock(response):
        return response.css('meta[itemprop="availability"][content="out_of_stock"]')

    @staticmethod
    def get_care(response):
        care_lines = response.css('div[itemprop=description]>div:last-child').css(' ::text').extract()
        care_lines = [line.strip() for line in care_lines]
        care_lines = ''.join(care_lines)
        return care_lines.split(". ")

    @staticmethod
    def get_description(response):
        return response.css('div[itemprop=description]>div:nth-child(2) ::text').extract()

    @staticmethod
    def get_retailer_sku(response):
        return response.css('span[data-code]::attr(data-code)').extract_first()

    @staticmethod
    def get_image_urls(response):
        image_paths = response.css('li[data-mimetype="image/jpeg"]::attr(data-detail)').extract()
        return [urljoin(response.url, path) for path in image_paths]

    @staticmethod
    def get_category(response):
        return response.css('#breadcrumb a::text').extract()

    @staticmethod
    def get_currency(response):
        return response.css('meta[itemprop="currency"]::attr(content)').extract_first()

    @staticmethod
    def get_price(response):
        price = response.css('meta[itemprop="price"]::attr(content)').extract_first()
        return 100 * float(price.replace(',', '.'))

    def colour_requests(self, response):
        colour_urls = response.css('.colors a::attr(href)').extract()
        trail = response.meta.get("trail", [])
        for url in colour_urls:
            request = response.follow(url, callback=self.parse)
            request.meta["trail"] = trail.copy().append(response.url)
            yield request
