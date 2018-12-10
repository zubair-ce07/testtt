import json
import re
from datetime import datetime

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from softsurroundings.items import SoftSurroundingsItem


class Mixin:
    allowed_domains = ["www.softsurroundings.com"]
    start_urls = ["http://www.softsurroundings.com/"]

    market = "US"
    retailer = "softsurroundings-us"


class SoftSurroundingsParser(Mixin):
    name = Mixin.retailer + "-parser"
    headers = {"X-Requested-With": "XMLHttpRequest"}

    def parse_product(self, response):
        item = SoftSurroundingsItem()
        item["uuid"] = self.product_id(response)
        item["name"] = self.product_name(response)
        item["category"] = self.product_category(response)
        item["crawl_id"] = self.get_crawl_id()
        item["spider_name"] = Mixin.retailer
        item["date"] = datetime.now().strftime("%Y-%m-%d")
        item["crawl_start_time"] = datetime.now().isoformat()
        item["url_orignal"] = response.url
        item["market"] = self.market
        item["retailer"] = self.retailer
        item["description"] = self.product_description(response)
        item["care"] = self.product_care(response)
        item["website_name"] = self.start_urls[0]
        item["skus"] = []
        item["image_urls"] = self.image_urls(response)
        item["meta"] = {
            "requests": self.color_requests(response, item) +
            self.size_category_requests(response, item)}

        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        requests = item["meta"]["requests"]
        yield (requests and requests.pop(0)) or item

    def size_category_requests(self, response, item):
        size_cat_ids = self.size_categories(response)
        if not size_cat_ids:
            return []

        return [response.follow(
            f"/p/{size_cat_id.lower()}/", self.parse_size_category,
            headers=self.headers, meta={"item": item}) for size_cat_id in size_cat_ids]

    def parse_size_category(self, response):
        item = response.meta["item"]
        item["meta"]["requests"] += self.color_requests(response, item)
        return self.next_request_or_item(item)

    def size_categories(self, response):
        css = "#sizecat a:not(.sel)::attr(id)"
        size_ids = response.css(css).extract()
        return [size.split("_")[1] for size in size_ids]

    def selected_size_cat_id(self, response):
        css = "#item[itemprop='productID']::text"
        return response.css(css).extract_first().lower()

    def color_requests(self, response, item):
        colors = self.color_ids(response)
        if not colors:
            return self.size_requests(response, item)

        size_cat = self.selected_size_cat_id(response)

        return [response.follow(
            f"/p/{size_cat}/{color}/", self.parse_colors,
            headers=self.headers, meta={"item": item}) for color in colors]

    def parse_colors(self, response):
        item = response.meta["item"]
        item["meta"]["requests"] += self.size_requests(response, item)
        return self.next_request_or_item(item)

    def color_ids(self, response):
        css = ".swatchlink img::attr(data-value)"
        return response.css(css).extract()

    def selected_color_id(self, response):
        css = "input[name*='specOne']::attr(value)"
        return response.css(css).extract_first()

    def size_requests(self, response, item):
        product_sizes = self.size_ids(response)
        if not product_sizes:
            return []

        size_cat = self.selected_size_cat_id(response)
        color_id = self.selected_color_id(response)

        return [response.follow(
            f"/p/{size_cat}/{color_id}{size}/", self.parse_size,
            headers=self.headers, meta={"item": item}) for size in product_sizes]

    def parse_size(self, response):
        item = response.meta["item"]
        item["skus"].append(self.skus(response))
        return self.next_request_or_item(item)

    def size_ids(self, response):
        css = "#size > a::attr(id)"
        sel_css = "input[name*='specTwo']::attr(value)"
        size_ids = response.css(css).extract()

        return [size_id.split("_")[1] for size_id in size_ids or [] if size_id] or response.css(sel_css).extract()

    def skus(self, response):
        skus = self.pricing_details(response)

        color_css = "#color b::text"
        skus["color"] = response.css(color_css).extract_first()

        size_css = "#size b::text"
        skus["size"] = response.css(size_css).extract_first()

        skus["availability"] = self.product_availability(response)
        skus["sku_id"] = f"{skus['color']}_{skus['size']}"

        return skus

    def product_availability(self, response):
        css = ".stockStatus b::text"
        return response.css(css).extract_first()

    def product_name(self, response):
        css = "span[itemprop='name']::text"
        return response.css(css).extract_first()

    def product_category(self, response):
        css = ".pagingBreadCrumb a::text"
        return response.css(css).extract()

    def product_description(self, response):
        css = ".productInfo::text, .productInfoDetails > ul ::text"
        return response.css(css).extract()

    def product_id(self, response):
        css = "input[name='uniqid']::attr(value)"
        return response.css(css).extract_first()

    def product_care(self, response):
        css = "#careAndContentInfo span::text"
        return response.css(css).extract()

    def pricing_details(self, response):
        pricing_details = {
            "price": self.product_price(response),
            "currency": self.currency_type(response)}

        prev_price = self.previous_price(response)
        if prev_price:
            pricing_details["previous_price"] = prev_price

        return pricing_details

    def product_price(self, response):
        css = "span[itemprop='price']::text"
        return int(float(response.css(css).extract_first()) * 100)

    def previous_price(self, response):
        css = ".ctntPrice::text"
        prev_price = response.css(css).extract_first()
        if prev_price:
            return int(float(re.findall("\d+\.?\d*", prev_price)[0]) * 100)

    def currency_type(self, response):
        css = "span[itemprop='priceCurrency']::attr(content)"
        return response.css(css).extract_first()

    def image_urls(self, response):
        css = ".alt_dtl::attr(href), .swatchlink img::attr(src)"
        return response.css(css).extract()

    def get_crawl_id(self):
        return f"softsurroundings-us-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj"


class SoftSurroundingsCrawler(CrawlSpider, Mixin):
    name = Mixin.retailer + "-crawler"
    parser = SoftSurroundingsParser()
    listing_css = [".dropdown-menu-wrapper"]
    product_css = [".product"]
    deny_re = ["gift-card"]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback="parse_pagination"),
        Rule(LinkExtractor(restrict_css=product_css, deny=deny_re), callback="parse_item"))

    def parse_pagination(self, response):
        total_pages_css = "form.thumbscroll input[name='page']::attr(value)"
        total_pages = response.css(total_pages_css).extract()

        url = f"{response.url}page-{total_pages[-1]}/" if total_pages else response.url
        yield Request(url, callback=self.parse)

    def parse_item(self, response):
        return self.parser.parse_product(response)
