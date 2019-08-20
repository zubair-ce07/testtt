import json
from datetime import datetime

from scrapy.spiders import Spider
from scrapy import Request

from calvinklein.items import CalvinKleinItem


class CalvinKleinParser(Spider):
    name = "calvinklein_parser"
    market = "AU"
    retailer = "calvinklein-au"
    language = "en"

    def parse(self, response):
        garment = CalvinKleinItem()
        garment["name"] = self.get_product_name(response)
        garment["description"] = self.get_product_description(response)
        garment["retailer_sku"] = self.get_retailer_sku(response)
        garment["image_urls"] = []
        garment["care"] = self.get_product_care(response)
        garment["url"] = response.url
        garment["lang"] = self.language
        garment["brand"] = self.get_product_brand(response)
        garment["category"] = self.get_product_category(response)
        garment["crawl_start_time"] = datetime.now().isoformat()
        garment["date"] = int(datetime.timestamp(datetime.now()))
        garment["crawl_id"] = self.get_crawl_id()
        garment["market"] = self.market
        garment["retailer"] = self.retailer
        garment["gender"] = self.get_product_gender(response)
        garment["skus"] = {}
        garment["meta"] = self.color_requests(response)
        garment["trail"] = response.meta["trail"]

        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta["garment"]
        garment["skus"].update(self.get_product_sku(response))
        garment["image_urls"] += self.get_product_images(response)
        return self.next_request_or_garment(garment)

    def clean_price(self, price):
        return int(price.strip().replace(".", ""))

    def clean_json(self, response):
        json_css = "script:contains('data-role=swatch-options')::text"
        raw_json = response.css(json_css).get()
        return raw_json.replace('\n', '')

    def get_product_name(self, response):
        css = ".page-title .base::text"
        return response.css(css).get()

    def get_product_description(self, response):
        css = "#ck\.product\.product\.info::text, #ck\.product\.product\.info li::text"
        return [description.strip() for description in response.css(css).getall()]

    def get_product_care(self, response):
        css = ".prod-attribute + .prod-attribute li::text"
        return response.css(css).getall()

    def get_retailer_sku(self, response):
        css = ".product-add-form form::attr(data-product-sku)"
        return response.css(css).get()

    def get_product_images(self, response):
        css = ".page-product-configurable"
        regex = 'full":"(.+?)"'
        return [image.replace("\\", "") for image in response.css(css).re(regex)]

    def get_product_brand(self, response):
        css = "meta::attr(content)"
        return response.css(css).getall()[3].split("| ")[-1]

    def get_product_category(self, response):
        css = "meta::attr(content)"
        return response.css(css).getall()[3].split("| ")

    def get_product_gender(self, response):
        css = "script:contains('getListFromLocalStorage')"
        regex = ': "(.+?)"'
        return response.css(css).re(regex)[-1]

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d-%H%M%s')}-medp"

    def color_requests(self, response):
        color_css = '.swatch-option.colour a::attr(href), link[rel="canonical"]::attr(href)'
        return [Request(url, callback=self.parse_color, dont_filter=True)
                for url in response.css(color_css).getall()]

    def next_request_or_garment(self, garment):
        requests = garment["meta"]

        if requests:
            request = requests.pop()
            request.meta["garment"] = garment
            yield request

        else:
            yield garment

    def get_previous_price(self, response):
        previous_price_css = '.price-wrapper[data-price-type="oldPrice"] span::text'
        previous_price = response.css(previous_price_css).get()
        return self.clean_price(previous_price.split('$')[1]) if previous_price else None

    def get_sale_price(self, response):
        price_css = '.price-wrapper[data-price-type="finalPrice"] span::text'
        return self.clean_price(response.css(price_css).get().split('$')[1])

    def get_price_currency(self, response):
        currency_css = '.price-wrapper[data-price-type="finalPrice"] span::text'
        return response.css(currency_css).get().split('$')[0]

    def get_product_pricing(self, response):
        previous_price = self.get_previous_price(response)
        pricing = {
            "price": self.get_sale_price(response),
            "currency": self.get_price_currency(response)
        }
        if previous_price:
            pricing['previous_price'] = previous_price

        return pricing

    def raw_sku(self, response):
        raw_skus = json.loads(self.clean_json(response))
        return raw_skus['[data-role=swatch-options]']['swatch-renderer-extended']['jsonConfig']

    def get_product_sku(self, response):
        skus = {}
        selected_color_css = ".current-swatch-text::text"

        selected_color = response.css(selected_color_css).get()
        common_sku = self.get_product_pricing(response)
        products = self.raw_sku(response)['attributes']['441']['options']

        common_sku["color"] = selected_color

        for size in products:
            sku = common_sku.copy()
            sku["size"] = size['label']

            if size['stock_status'] == "0":
                sku["out_of_stock"] = True
            skus[f"{sku['color']}_{sku['size']}"] = sku

        if not skus:
            common_sku["size"] = 'Single_size'
            skus[f"{common_sku['color']}_{common_sku['size']}"] = common_sku

        return skus
