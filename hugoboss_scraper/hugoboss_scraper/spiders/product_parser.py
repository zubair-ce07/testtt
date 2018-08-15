from json import loads as json_loads

from scrapy import Spider
from w3lib.url import url_query_cleaner as w3cleaner


class Parser(Spider):
    name = "parser"
    scraped_ids = []

    def parse(self, response):
        product = {}
        product_data = self.get_product_json(response)
        if product_data["id"] in self.scraped_ids:
            return
        self.scraped_ids.append(product_data["id"])
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

    @staticmethod
    def item_or_request(response):
        if not response.meta["pending_color_reqs"]:
            return response.meta["product"].copy()
        next_color_req = response.meta["pending_color_reqs"].pop()
        next_color_req.meta["product"] = response.meta["product"].copy()
        next_color_req.meta["pending_color_reqs"] = response.meta["pending_color_reqs"].copy()
        return next_color_req

    def parse_colour(self, response):
        response.meta["product"]["skus"].update(self.get_skus(response))
        response.meta["product"]["image_urls"] += self.get_image_urls(response)
        return self.item_or_request(response)

    def get_skus(self, response):
        skus = {}
        common_sku = {}
        product_data = self.get_product_json(response)
        sku_variant = product_data["variant"]
        common_sku["price"] = product_data["price"]
        common_sku["currency"] = self.get_currency(response)
        common_sku["colour"] = self.get_colour(response)
        common_sku["size"] = "One Size"
        discount = product_data["metric3"]
        if discount:
            common_sku["previous_prices"] = [product_data["price"] + discount]
        sizes = response.css('.swatch-list__size')
        if not sizes:
            skus[f"{sku_variant}_One Size"] = common_sku
            return skus
        for size in sizes:
            sku = common_sku.copy()
            sku["size"] = size.css('::text').extract_first().strip()
            if size.css('[class*="unselectable"]'):
                sku["out_of_stock"] = True
            skus[f'{sku_variant}_{sku["size"]}'] = sku
        return skus

    @staticmethod
    def get_currency(response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    @staticmethod
    def get_colour(response):
        variation_json = response.css('.product-variations::attr(data-current)').extract_first()
        json_object = json_loads(variation_json)
        return json_object["color"]["displayValue"]

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
        paragraph = response.css('div.product-container__text__description::text').extract_first(default='')
        return [line.strip() for line in paragraph.strip().split('.\n')]

    @staticmethod
    def get_care(response):
        material_care = response.css('.materialCare>.product-container__text::text').extract_first()
        material_care = material_care.strip().split(", ") if material_care else []
        return material_care + response.css('.accordion__care-icon__text::text').extract()

    @staticmethod
    def get_product_json(response):
        json_string = response.css('div[data-as-product]::attr(data-as-product)').extract_first()
        json_string.replace('&quot;', '"')
        return json_loads(json_string)

    def colour_requests(self, response):
        colour_urls = response.css('.swatch-list__button--is-empty>a::attr(href)').extract()
        colour_reqs = []
        for url in colour_urls:
            request = response.follow(w3cleaner(url), callback=self.parse_colour, dont_filter=True)
            if response.url != request.url:
                colour_reqs.append(request)
        return colour_reqs
