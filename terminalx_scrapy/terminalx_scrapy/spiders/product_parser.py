from json import loads as json_loads

from scrapy import Spider
from w3lib.url import url_query_cleaner as w3cleaner


class Parser(Spider):
    name = "parser"
    scraped_ids = set()

    def parse(self, response):
        product = {}
        product_data = self.get_product_json(response)

        if self.id_exists(product_data["id"]):
            return

        product["retailer_sku"] = product_data["id"]
        product["name"] = product_data["name"] or ""
        product["image_urls"] = self.get_image_urls(response)
        product["lang"] = "en"
        product["gender"] = product_data["gender"]
        product["category"] = self.get_categories(response)
        product["industry"] = None
        product["brand"] = product_data["brand"]
        product["url"] = response.url
        product["market"] = "US"
        product["trail"] = response.meta["trail"]
        product["retailer"] = "hugoboss"
        product["url_original"] = response.url
        product["description"] = self.get_description(response)
        product["care"] = self.get_care(response)
        product["skus"] = self.get_skus(response)
        response.meta["pending_color_reqs"] = self.colour_requests(response)
        response.meta["product"] = product
        return self.item_or_request(response)

    def parse_colour(self, response):
        response.meta["product"]["skus"].update(self.get_skus(response))
        response.meta["product"]["image_urls"] += self.get_image_urls(response)
        return self.item_or_request(response)

    @staticmethod
    def item_or_request(response):

        if not response.meta["pending_color_reqs"]:
            return response.meta["product"].copy()

        next_color_req = response.meta["pending_color_reqs"].pop()
        next_color_req.meta["product"] = response.meta["product"].copy()
        next_color_req.meta["pending_color_reqs"] = response.meta["pending_color_reqs"].copy()
        return next_color_req

    def get_skus(self, response):
        skus = {}
        product_data = self.get_product_json(response)
        sku_variant = product_data["variant"]
        sizes_s = response.css('.swatch-list__size')
        common_sku = self.get_common_sku(response, product_data)

        if not sizes_s:
            skus[f"{sku_variant}_One Size"] = common_sku
            skus[f"{sku_variant}_One Size"]["size"] = "One Size"
            return skus

        for size in sizes_s:
            sku = common_sku.copy()
            sku["size"] = size.css('::text').extract_first().strip()
            if size.css('[class*="unselectable"]'):
                sku["out_of_stock"] = True
            skus[f'{sku_variant}_{sku["size"]}'] = sku

        return skus

    def get_common_sku(self, response, product_data):
        common_sku = {}

        discount = product_data["metric3"]
        if discount:
            common_sku["previous_prices"] = [product_data["price"] + discount]

        common_sku["price"] = product_data["price"]
        common_sku["currency"] = self.get_currency(response)
        common_sku["colour"] = self.get_colour(response)
        return common_sku

    @staticmethod
    def get_currency(response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    @staticmethod
    def get_colour(response):
        variation = response.css('.product-variations::attr(data-current)').extract_first()
        return json_loads(variation)["color"]["displayValue"]

    @staticmethod
    def get_categories(response):
        unique_breadcrumbs = set(response.css('.breadcrumb__link::attr(title)').extract())
        unique_breadcrumbs.remove("Home")
        unique_breadcrumbs.remove("Shop")
        return list(unique_breadcrumbs)

    @staticmethod
    def get_image_urls(response):
        image_urls = response.css('img.slider-item__image::attr(src)').extract()
        return [w3cleaner(url) for url in image_urls]

    @staticmethod
    def get_description(response):
        description = response.css('div.product-container__text__description::text').extract_first(default='')
        return [line.strip() for line in description.strip().split('.\n')]

    @staticmethod
    def get_care(response):
        material_care = response.css('.materialCare>.product-container__text::text').extract_first()
        material_care = material_care.strip().split(", ") if material_care else []
        return material_care + response.css('.accordion__care-icon__text::text').extract()

    @staticmethod
    def get_product_json(response):
        raw_product = response.css('div[data-as-product]::attr(data-as-product)').extract_first()
        raw_product.replace('&quot;', '"')
        return json_loads(raw_product)

    def colour_requests(self, response):
        colour_urls = response.css('.swatch-list__button--is-empty>a::attr(href)').extract()
        colour_reqs = []

        for url in colour_urls:
            colour_reqs.append(response.follow(w3cleaner(url), callback=self.parse_colour, dont_filter=True))

        return colour_reqs

    def id_exists(self, product_id):
        if product_id in self.scraped_ids:
            return True
        self.scraped_ids.add(product_id)
        return False
