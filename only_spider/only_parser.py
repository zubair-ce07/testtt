import re
from datetime import datetime

from scrapy.spiders import Spider, Request
from w3lib.url import url_query_cleaner, add_or_replace_parameter

from only.only_items import OnlyItem


class OnlyParser(Spider):
    name = "only_parser"

    currency = "GB"
    retailer = "only-ca"
    lang = "en"
    market = "UK"

    def parse(self, response):
        garment = OnlyItem()
        garment["name"] = self.get_product_name(response)
        garment["description"] = self.get_product_description(response)
        garment["retailer_sku"] = self.get_retailer_sku(response)
        garment["image_urls"] = []
        garment["care"] = self.get_product_care(response)
        garment["url"] = response.url
        garment["lang"] = self.lang
        garment["brand"] = self.get_product_brand(response)
        garment["category"] = self.get_product_category(response)
        garment["crawl_start_time"] = datetime.now().isoformat()
        garment["date"] = int(datetime.timestamp(datetime.now()))
        garment["crawl_id"] = self.get_crawl_id()
        garment["market"] = self.market
        garment["retailer"] = self.retailer
        garment["gender"] = self.get_gender(response)
        garment["price"] = self.get_sale_price(response)
        garment["skus"] = {}
        garment["meta"] = self.color_requests(response)

        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta["garment"]
        garment["skus"].update(self.get_product_sku(response))
        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta["garment"]
        garment["image_urls"] += self.get_image_urls(response)
        garment["meta"] += self.size_requests(response)
        return self.next_request_or_garment(garment)

    def clean(self, raw_list):
        regex = r"\r\n|\r|\n|\-|\  +"
        return [re.sub(regex, "", string.strip()) for string in raw_list]

    def clean_price(self, raw_price):
        return raw_price.split("£ ", 1)[1].replace(".", "")

    def get_product_name(self, response):
        return response.css(".product-name--visible::text").get()

    def get_product_description(self, response):
        css = '.pdp-description__text__short::text'
        return self.clean(response.css(css).getall())

    def get_product_care(self, response):
        css = '.pdp-description__list__item::text'
        return self.clean(response.css(css).getall())

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d-%H%M%s')}-medp"

    def get_product_brand(self, response):
        css = '.servicebar__logo__align--middle::attr(alt)'
        return response.css(css).get()

    def get_retailer_sku(self, response):
        css = '.pdp-description__text__value--article-nr::text'
        return response.css(css).re_first('Number: (.+)')

    def get_product_category(self, response):
        css = "script:contains('@context')"
        regex = 'category":"(.+?)"'
        return [category.strip() for category in response.css(css).re_first(regex).split(">")]

    def get_gender(self, response):
        css = "script:contains('@context')"
        regex = 'category":"(.+?)"'
        return response.css(css).re_first(regex).split(" ")[0]

    def get_image_urls(self, response):
        css = ".product-images__main__image img::attr(data-src)"
        regex = "c_.+?auto/"
        return [re.sub(regex, '', url_query_cleaner(url)) for url in response.css(css).getall()]

    def get_previous_price(self, response):
        previous_price_css = ".nonsticky-price__container--visible .value__price--discount::text"
        previous_price = response.css(previous_price_css).get()
        return self.clean_price(previous_price) if previous_price else None

    def get_sale_price(self, response):
        price_css = ".nonsticky-price__container--visible .value__price::text, " \
                    ".nonsticky-price__container--visible .value__price--discounted::text"
        return self.clean_price(response.css(price_css).get())

    def get_product_pricing(self, response):
        previous_price = self.get_previous_price(response)
        pricing = {
            "price": self.get_sale_price(response),
            "currency": self.currency
        }
        if previous_price:
            pricing['previous_price'] = previous_price

        return pricing

    def next_request_or_garment(self, garment):
        requests = garment["meta"]

        if requests:
            request = requests.pop()
            request.meta["garment"] = garment
            yield request

        else:
            yield garment

    def color_requests(self, response):
        color_css = ".swatch__item--unavailable-colorpattern .js-swatch-item-link::attr(data-href)," \
                    ".swatch__item--selectable-colorpattern .js-swatch-item-link::attr(data-href)," \
                    ".swatch.size .js-swatch-item-link::attr(data-href)"
        return [Request(add_or_replace_parameter(url, 'format', 'ajax'), callback=self.parse_color)
                for url in response.css(color_css).getall()]

    def size_requests(self, response):
        size_css = ".swatch.size .swatch__item-inner-text__text-container::text"
        return [Request(add_or_replace_parameter(response.url, 'dwvar_size', size), callback=self.parse_size,
                        dont_filter=True) for size in response.css(size_css).getall()]

    def get_product_sku(self, response):
        skus = {}
        common_sku = self.get_product_pricing(response)

        color_css = ".swatch__item--selected-colorpattern .js-swatch-item-link::attr(title)," \
                    ".swatch__item--selected.swatch__item--unavailable-colorpattern .js-swatch-item-link::attr(title)"
        size_css = ".swatch__item--selected .js-swatch-item-link::attr(title)"
        out_of_stock_css = ".swatch__item--selected.swatch__item--unavailable .js-swatch-item-link"

        common_sku["color"] = response.css(color_css).re_first('Colour: (.+)')
        common_sku["size"] = response.css(size_css).re_first('Size: (.+)')

        if not response.css(".swatch.length"):
            sku = common_sku.copy()

            if response.css(out_of_stock_css):
                sku["out_of_stock"] = True

            skus[f"{sku['color']}_{sku['size']}"] = sku
            return skus

        for len_sel in response.css(".swatch.length .js-swatch-item"):
            sku = common_sku.copy()

            length = len_sel.css('.swatch__item-inner-text__text-container::text').get()
            sku["size"] = f"{common_sku['size']}/{length}"

            if len_sel.css('.swatch__item--selectable.swatch__item--unavailable'):
                sku["out_of_stock"] = True

            skus[f"{sku['color']}_{sku['size']}"] = sku

        return skus
