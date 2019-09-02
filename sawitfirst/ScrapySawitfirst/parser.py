from copy import copy
from copy import deepcopy
from json import loads
from re import findall
from urllib.parse import urljoin

from scrapy import Request
from scrapy.http import JSONRequest
from scrapy.spiders import Spider

from ScrapySawitfirst.items import Item


class SawItFirstParser(Spider):
    name = "sawitfirstitemparser"
    gender = "women"
    color_request_url = "https://4uiusmis27.execute-api.eu-central-1.amazonaws.com/isaw/get-colours"
    product_request_url = "https://www.isawitfirst.com/products/"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://www.isawitfirst.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
                       (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.99"
    }
    raw_care = ["%", "machine", "wash", "wipe", "clean", "hand"]

    def parse(self, response):
        product = Item()
        product['retailer_sku'] = self.retailer_sku(response)
        product['gender'] = self.gender
        product['category'] = self.category(response)
        product['brand'] = self.brand(response)
        product['url'] = response.url
        product['name'] = self.name(response)
        product['description'] = self.description(response)
        product['care'] = self.care(response)
        product['image_urls'] = self.image_urls(response)
        product['price'] = self.price(response)
        product['previous_prices'] = self.previous_prices(response)
        product['currency'] = self.currency(response)
        product['skus'] = {}
        product['meta'] = []
        return self.request_colours(response, product)

    def parse_color_requests(self, response):
        product = response.meta["product"]
        colours = loads(response.text)
        for colour in colours["products"]:
            url = urljoin(self.product_request_url, colour['handle'])
            request = Request(url, callback=self.parse_skus)
            request.meta['colours'] = colours
            product['meta'].append(request)
        return self.next_request_or_product(product)

    def parse_skus(self, response):
        product = response.meta["product"]
        colours = response.meta["colours"]
        colour = self.product_skus(response, colours)
        product['skus'].update(colour)
        return self.next_request_or_product(product)

    def request_colours(self, response, product):
        form_data = {
            "jl_numbers": response.css(".product-info-block::attr(data-jlnumber)").extract(),
            "site": "isawitfirst.com"
        }
        headers = self.headers
        headers["Referer"] = response.url
        request = JSONRequest(self.color_request_url,
                              callback=self.parse_color_requests,
                              data=form_data, headers=self.headers
                              )
        request.meta["product"] = product
        return request

    def next_request_or_product(self, product):
        if len(product['meta']) > 0:
            request = product['meta'].pop(0)
            request.meta["product"] = product
            return request
        else:
            return product

    def retailer_sku(self, response):
        return response.css(".product-sku > ::text").extract_first()

    def category(self, response):
        categories_raw = findall("Categories: (.+),", response.text)[0]
        return findall(r'"\s*([^"]*?)\s*"', categories_raw)

    def brand(self, response):
        text = response.css(".analytics").extract_first()
        return findall(r'"brand":"(.+)","', text)[0]

    def name(self, response):
        return response.css("[itemprop=name]::attr(content)").extract_first()

    def description(self, response):
        return response.xpath('//*[*[@class="product-description-title"]]/p/text()').extract()

    def care(self, response):
        description = response.xpath('//*[*[@class="product-description-title"]]/p/text()').extract()
        return [d for d in description if any(cr in d.lower() for cr in self.raw_care)]

    def image_urls(self, response):
        return response.css(".slide-item img::attr(src)").getall()

    def price(self, response):
        price_text = response.css("[data-handle=sale-price]::text").extract_first()
        return self.format_price(price_text)

    def previous_prices(self, response):
        prices = response.css(".old-price::text").extract()
        prices = set([self.format_price(p) for p in prices])
        return list(prices)

    def format_price(self, price):
        return int(price.replace(u'\u00A3', '').replace(".", ''))

    def currency(self, response):
        return response.css('[property=og\:price\:currency]::attr(content)').extract_first()

    def color(self, response, colours):
        for product in colours["products"]:
            if product['handle'] in response.url:
                return product["colour_name"]

    def stock(self, response):
        quantities = [int(q) for q in response.css(".product-size option::attr(data-quantity)").extract()]
        sizes = [s.strip() for s in response.css(".size-list .value::text").extract() if s.strip()]
        stock = []
        for size, quantity in zip(sizes, quantities):
            stock.append((size, quantity))
        return stock

    def product_skus(self, response, colours):
        skus = {}
        color = self.color(response, colours)
        price = self.price(response)
        previous_prices = self.previous_prices(response)
        currency = self.currency(response)
        stock = self.stock(response)
        sku = {
            "colour": color,
            "price": price,
            'previous_prices': previous_prices,
            "currency": currency
        }
        for size, quantity in stock:
            sku = copy(sku)
            sku["size"] = size
            sku["out_of_stock"] = quantity == 0
            skus[f"{color}_{size}"] = deepcopy(sku)
        return skus
