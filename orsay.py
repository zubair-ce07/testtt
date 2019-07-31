import re
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from orsay.items import OrsayItem


class OrsaySpider(CrawlSpider):
    name = "orsay"
    allowed_domains = ["orsay.com"]
    start_urls = [
        "https://www.orsay.com/de-de/",
    ]

    retailer = "orsay-de"
    market = "DE"
    language = "de"

    gender = "Women"

    restrict_home_css = [".level-1"]
    restrict_product_css = [".thumb-link"]

    rules = (
        Rule(LinkExtractor(restrict_css=restrict_home_css)),
        Rule(LinkExtractor(restrict_css=restrict_product_css), callback='parse_item'),)

    def parse_item(self, response):
        garment = OrsayItem()
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
        garment["gender"] = self.gender
        garment["skus"] = {}
        garment["meta"] = self.get_sku_reqs(response, garment)

        return self.yield_sku_reqs(garment)

    def clean(self, raw_list):
        return [re.sub(r'\s+', '', string) for string in raw_list]

    def clean_price(self, price):
        return re.sub(r'\s+', '', str(price)).replace(",", "")

    def get_product_name(self, response):
        css = ".product-name::text"
        return response.css(css).get()

    def get_product_description(self, response):
        css = ".with-gutter::text"
        return response.css(css).getall()

    def get_retailer_sku(self, response):
        css = ".product-sku::text"
        return response.css(css).get().split(" ", 1)[1]

    def get_image_urls(self, response):
        css = ".primary-image::attr(src)"
        return [urlparse(url).netloc+urlparse(url).path for url in response.css(css).getall()]

    def get_product_care(self, response):
        css = ".product-material p::text"
        return self.clean(response.css(css).getall())

    def get_product_brand(self, response):
        css = ".header-logo img::attr(alt)"
        return response.css(css).get()

    def get_product_category(self, response):
        css = ".breadcrumb-element-link span::text"
        return response.css(css).getall()[1]

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d-%H%M%s')}-medp"

    def get_previous_price(self, response):
        previous_price_css = ".price-standard::text"
        previous_price = response.css(previous_price_css).get()
        if previous_price:
            return {"previous_price": self.clean_price(previous_price.split(" ", 1)[0])}

    def get_product_pricing(self, response):
        price_css = ".price-sales::text"
        currency_css = ".country-currency::text"
        pricing = self.get_previous_price(response) or {}
        pricing.update({
            "price": self.clean_price(response.css(price_css).get().split(" ", 1)[0]),
            "currency": response.css(currency_css).get()
        })
        return pricing

    def get_sku_reqs(self, response, garment):
        color_urls_css = ".swatchanchor.js-color-swatch::attr(href)"
        return [Request(url, callback=self.update_sku, meta={"garment": garment}, dont_filter=True) for url in
                response.css(color_urls_css).getall()]

    def update_sku(self, response):
        garment = response.meta["garment"]
        garment["skus"].update(self.get_product_sku(response))
        garment["image_urls"] += (self.get_image_urls(response))
        return self.yield_sku_reqs(garment)

    def yield_sku_reqs(self, garment):
        sku_reqs = garment["meta"]
        yield sku_reqs and sku_reqs.pop() or garment

    def get_product_sku(self, response):
        skus = {}
        selected_color_css = ".selected-value::text"
        sizes_css = ".swatches.size .swatchanchor::text"
        out_of_stock_sizes_css = ".swatches.size .unselectable .swatchanchor::text"

        selected_color = response.css(selected_color_css).get()
        out_of_stock_sizes = self.clean(response.css(out_of_stock_sizes_css).getall())
        common_sku = self.get_product_pricing(response)
        common_sku["color"] = selected_color

        for size in self.clean(response.css(sizes_css).getall()) or ["single_size"]:
            sku = common_sku.copy()
            sku["size"] = size
            if size in out_of_stock_sizes:
                sku["out_of_stock"] = True
            skus[f"{sku['color']}_{sku['size']}"] = sku

        return skus
