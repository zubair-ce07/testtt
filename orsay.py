from w3lib.url import url_query_cleaner
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

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

    current_products = 0

    listings_css = [".level-1"]
    products_css = [".thumb-link"]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="pagination"),
        Rule(LinkExtractor(restrict_css=products_css), callback="parse_item"),
    )

    def pagination(self, response):
        pagination_details = self.get_pagination_details(response)
        if pagination_details:
            self.current_products += pagination_details['product_size']

            while self.current_products < pagination_details['max_products']:
                next_page = pagination_details['pagination_url'] + str(self.current_products)
                self.current_products += pagination_details['product_size']
                yield Request(next_page, callback=self.parse)

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
        garment["meta"] = self.color_requests(response, garment)

        return self.next_request_or_garment(garment)

    def clean(self, raw_list):
        return [string.strip() for string in raw_list]

    def clean_price(self, price):
        return price.strip().replace(",", "")

    def get_pagination_details(self, response):
        self.current_products = 0
        pagination_url = response.url + "?sz="
        max_products_css = ".js-pagination-product-count::attr(data-count)"
        product_size_css = "#search-result-items > li:nth-child(72)::attr(data-idx)"
        product_size = response.css(product_size_css).get()
        max_products = response.css(max_products_css).get()
        if max_products:
            return {
                "pagination_url": pagination_url,
                "max_products": int(max_products),
                "product_size": int(product_size)
            }

    def get_product_name(self, response):
        css = ".product-name::text"
        return response.css(css).get()

    def get_product_description(self, response):
        css = ".with-gutter::text"
        return self.clean(response.css(css).getall())

    def get_retailer_sku(self, response):
        css = ".product-sku::text"
        return response.css(css).get().split(" ", 1)[1]

    def get_image_urls(self, response):
        css = ".primary-image::attr(src)"
        return [url_query_cleaner(url) for url in response.css(css).getall()]

    def get_product_care(self, response):
        css = ".product-material p::text"
        return self.clean(response.css(css).getall())

    def get_product_brand(self, response):
        css = ".header-logo img::attr(alt)"
        return response.css(css).get()

    def get_product_category(self, response):
        css = ".breadcrumb-element-link span::text"
        return response.css(css).getall()

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d-%H%M%s')}-medp"

    def get_previous_price(self, response):
        previous_price_css = ".price-standard::text"
        previous_price = response.css(previous_price_css).get()
        if previous_price:
            return self.clean_price(previous_price.split(" ", 1)[0])

    def get_sale_price(self, response):
        price_css = ".price-sales::text"
        return self.clean_price(response.css(price_css).get().split(" ", 1)[0])

    def get_price_currency(self, response):
        currency_css = ".country-currency::text"
        return response.css(currency_css).get()

    def get_product_pricing(self, response):
        pricing = {
            "price": self.get_sale_price(response),
            "currency": self.get_price_currency(response)
        }
        if self.get_previous_price(response):
            pricing.update({"previous_price": self.get_previous_price(response)})

        return pricing

    def color_requests(self, response, garment):
        color_css = ".swatchanchor.js-color-swatch::attr(href)"
        return [Request(url, callback=self.parse_color, meta={"garment": garment}, dont_filter=True) for url in
                response.css(color_css).getall()]

    def parse_color(self, response):
        garment = response.meta["garment"]
        garment["skus"].update(self.get_product_sku(response))
        garment["image_urls"] += self.get_image_urls(response)
        return self.next_request_or_garment(garment)

    def next_request_or_garment(self, garment):
        sku_reqs = garment["meta"]
        yield (sku_reqs and sku_reqs.pop()) or garment

    def get_product_sku(self, response):
        skus = {}
        selected_color_css = ".selected-value::text"
        sizes_css = ".swatches.size .swatchanchor::text"
        out_of_stock_sizes_css = ".swatches.size .unselectable .swatchanchor::text"

        selected_color = response.css(selected_color_css).get()
        common_sku = self.get_product_pricing(response)
        common_sku["color"] = selected_color

        for size in response.css(sizes_css) or ["single_size"]:
            sku = common_sku.copy()
            sku["size"] = size.get().strip()
            if size in response.css(out_of_stock_sizes_css):
                sku["out_of_stock"] = True
            skus[f"{sku['color']}_{sku['size']}"] = sku

        return skus
