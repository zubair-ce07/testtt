import json
import re
from datetime import datetime

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from vans.items import VansItem


class Mixin:
    allowed_domains = ["vans.fr"]
    start_urls = ["http://www.vans.fr/"]
    retailer = "vans-fr"
    market = "FR"


class VansParser(Mixin):
    name = Mixin.retailer + "-parser"

    def parse_product(self, response):
        item = VansItem()
        item["uuid"] = self.product_id(response)
        item["name"] = self.product_name(response)
        item["gender"] = self.get_gender(response)
        item["market"] = self.market
        item["retailer"] = self.retailer
        item["retailer_sku"] = self.retailer_sku(response)
        item["description"] = self.product_description(response)
        item["care"] = self.product_care(response)
        item["category"] = self.product_category(response)
        item["crawl_id"] = self.get_crawl_id()
        item["spider_name"] = Mixin.retailer
        item["date"] = datetime.now().strftime("%Y-%m-%d")
        item["crawl_start_time"] = datetime.now().isoformat()
        item["url_orignal"] = response.url
        item["skus"] = []
        item["image_urls"] = []
        item["meta"] = self.color_requests(response, item)

        return self.next_request_or_item(item)

    def skus(self, response):
        sizes = self.product_sizes(response)
        skus = []
        for size in sizes:
            sku = self.product_pricing(response)
            sku["color"] = self.color_name(response)
            sku["size"] = size
            sku["sku_id"] = f"{sku['color']}_{size}"
            skus.append(sku)
        return skus

    def next_request_or_item(self, item):
        color_requests = item["meta"]
        yield (color_requests and color_requests.pop(0)) or item

    def parse_colors(self, response):
        item = response.meta["item"]
        item["skus"] += self.skus(response)
        item["image_urls"] += self.image_urls(response)
        return self.next_request_or_item(item)

    def product_id(self, response):
        css = ".step-container::attr(data-product-id)"
        return response.css(css).extract_first()

    def retailer_sku(self, response):
        css = "input[name='productCode']::attr(value)"
        return response.css(css).extract_first()

    def product_name(self, response):
        css = "h1.product-info-js::text"
        return response.css(css).extract_first()

    def product_price(self, response):
        css = "meta[property='og:price:amount']::attr(content)"
        return int(float(response.css(css).extract_first()) * 100)

    def previous_price(self, response):
        script = "var itemPrices = (.+?);\n"
        price_details = json.loads(re.findall(script, response.body.decode("utf-8"))[0])
        return int(float(price_details[self.product_id(response)][
            "pricing"]["default"]["lowListPriceNumeric"]) * 100)

    def product_description(self, response):
        css = ".desc-container ::text"
        return response.css(css).extract_first()

    def product_care(self, response):
        css = ".desc-container ::text"
        return self.clean(response.css(css).extract()[-1])

    def product_category(self, response):
        css = "#product-attr-form::attr(data-seo-category)"
        return response.css(css).extract()

    def color_name(self, response):
        css = ".attr-selected-color-js::text"
        return response.css(css).extract_first()

    def product_sizes(self, response):
        css = ".swatches .attr-box::attr(data-attribute-value)"
        return response.css(css).extract()

    def get_gender(self, response):
        css = "#product-attr-form::attr(data-master-category-identifier)"
        return response.css(css).extract_first()

    def get_crawl_id(self):
        return f"vans-us-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj"

    def currency_type(self, response):
        css = "meta[property='og:price:currency']::attr(content)"
        return response.css(css).extract_first()

    def product_pricing(self, response):
        pricing_details = {
            "price": self.product_price(response),
            "currency": self.currency_type(response)}

        prev_price = self.previous_price(response)
        if prev_price != pricing_details["price"]:
            pricing_details["previous_price"] = prev_price
        return pricing_details

    def image_urls(self, response):
        css = ".vfdp-s7-viewer-preload-image::attr(src)"
        urls = response.css(css).extract()
        return [response.urljoin(url) for url in urls]

    def color_requests(self, response, item):
        urls = response.css("button img::attr(data-product-url)").extract()
        return [Request(url, callback=self.parse_colors, meta={"item": item}) for url in urls]

    def clean(self, dirty_strs):
        return [re.sub(':\s+', ' ', text).strip() for text in dirty_strs.split(";")]


class VansCrawler(CrawlSpider, Mixin):
    name = Mixin.retailer + "-crawler"
    parser = VansParser()
    listings_css = [".sub-category"]
    product_css = [".product-block-figure"]
    deny_re = [".html"]
    PAGE_SIZE = 48

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback="parse_pagination"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )

    def parse_pagination(self, response):
        pages = self.page_count(response)
        for page in range(0, pages, self.PAGE_SIZE):
            url = f"{response.url}#esp_pg={page//self.PAGE_SIZE}"
            yield Request(url, callback=self.parse, dont_filter=True)

    def parse_item(self, response):
        return self.parser.parse_product(response)

    def page_count(self, response):
        css = ".header-result-counter ::text"
        return int(response.css(css).re_first("\d+") or '0')
