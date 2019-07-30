import re
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

    product_css = ".thumb-link"
    deny_urls = ['/trends/', 'pref', 'size', 'faq', 'help']

    rules = (
        Rule(LinkExtractor(allow=('/produkte/', '.header-in'), deny=deny_urls)),
        Rule(LinkExtractor(allow=('.html', product_css), deny=deny_urls), callback='parse_item'),)

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
        garment["price"] = 0
        garment["skus"] = {}
        garment["meta_data"] = self.get_sku_reqs(response, garment)

        return self.yield_sku_reqs(garment)

    def clean(self, raw_list):
        return list(map(lambda string: re.sub(r'\s+', '', string), raw_list))

    def clean_price(self, price):
        price = re.sub(r'\s+', '', str(price))
        return format(float(re.sub(',', '.', str(price))), '.2f')

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
        return list(map(lambda url: url.split("?")[0], response.css(css).getall()))

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

    def get_product_pricing(self, response):
        price_css = ".price-sales::text"
        currency_css = ".country-currency::text"
        previous_price_css = ".price-standard::text"
        previous_price = response.css(previous_price_css).get()

        pricing = {
            "price": self.clean_price(response.css(price_css).get().split(" ", 1)[0]),
            "currency": response.css(currency_css).get()
        }
        if previous_price:
            pricing["previous_price"] = self.clean_price(previous_price.split(" ", 1)[0])
        return pricing

    def get_sku_reqs(self, response, garment):
        color_urls_css = ".swatchanchor.js-color-swatch::attr(href)"
        colors_urls = response.css(color_urls_css).getall()
        total_reqs = []

        for url in colors_urls:
            total_reqs.append(Request(url, callback=self.update_sku, meta={"garment": garment}, dont_filter=True))
        return total_reqs

    def update_sku(self, response):
        garment = response.meta["garment"]
        garment["skus"].update(self.get_product_sku(response))
        garment["image_urls"] += (self.get_image_urls(response))
        return self.yield_sku_reqs(garment)

    def yield_sku_reqs(self, garment):
        sku_reqs = garment["meta_data"]
        if sku_reqs:
            sku_req = sku_reqs[0]
            del sku_reqs[0]
            yield sku_req
        else:
            garment["price"] = min(garment["skus"][sku]["price"] for sku in garment["skus"])
            yield garment

    def get_product_sku(self, response):
        skus = {}
        selected_color_css = ".selected-value::text"
        size_css = ".swatches.size .selectable .swatchanchor::text"
        stock_status_css = ".in-stock-msg::text"

        stock_status = response.css(stock_status_css).get()
        selected_color = response.css(selected_color_css).get()
        sizes = self.clean(response.css(size_css).getall())
        common_sku = self.get_product_pricing(response)
        common_sku["color"] = selected_color
        if not sizes:
            sizes = ["single_size"]

        for size in sizes:
            sku = common_sku.copy()
            sku["size"] = size
            sku["availability"] = stock_status
            skus[f"{sku['color']}_{sku['size']}"] = sku

        return skus
