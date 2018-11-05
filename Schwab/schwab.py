import json
import re
import urllib.parse
from datetime import datetime

from schwab.items import SchwabItem
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Mixin:
    name = "schwab"
    allowed_domains = ["www.schwab.de"]
    start_urls = ["http://www.schwab.de/"]
    retailer = "schwab-gr"
    market = "GR"

    category_req_url_t = "https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true"
    color_req_url_t = "https://www.schwab.de/index.php?{0}"


class SchwabParser(Mixin):
    name = Mixin.name + "-parser"

    def parse_product(self, response):
        item = SchwabItem()
        item["uuid"] = self.product_id(response)
        item["name"] = self.product_name(response)
        item["brand"] = self.product_brand(response)
        item["category"] = self.product_category(response)
        item["crawl_id"] = self.get_crawl_id()
        item["spider_name"] = Mixin.name
        item["date"] = datetime.now().strftime("%Y-%m-%d")
        item["crawl_start_time"] = datetime.now().isoformat()
        item["url_orignal"] = response.url
        item["url"] = self.product_url(response)
        item["market"] = self.market
        item["retailer"] = self.retailer
        item["description"] = self.product_description(response)
        item["care"] = self.product_care(response)
        item["skus"] = []
        item["image_urls"] = []
        item["meta"] = self.color_requests(response, item)

        return self.next_request_or_item(item)

    def skus(self, response):
        sizes = self.clean(self.product_sizes(response))
        if not sizes:
            sizes.append("One_size")
        skus = []
        for size in sizes:
            sku = self.product_pricing(response)
            sku["color"] = self.color_name(response)
            sku["size"] = size
            sku["sku_id"] = f"{sku['color']}_{size}"
            skus.append(sku)
        return skus

    def parse_colors(self, response):
        item = response.meta["item"]
        item["skus"] += self.skus(response)
        item["image_urls"] += self.image_urls(response)
        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        color_requests = item["meta"]
        yield (color_requests and color_requests.pop(0)) or item

    def color_requests(self, response, item):
        colors = self.colors_varsel_id(response)
        if not colors:
            colors.append("One_Color")
        color_requests = []
        parameters = {
            "cl": "oxwarticledetails", "ajaxdetails": "adsColorChange",
            "anid": self.article_id(response), "varselid[0]": "",
            "varselid[1]": self.version_varsel_id(response)}

        for color in colors:
            parameters["varselid[2]"] = color
            url = self.color_req_url_t.format(urllib.parse.urlencode(parameters))
            color_requests.append(Request(
                url, callback=self.parse_colors, meta={"item": item}))
        return color_requests

    def colors_varsel_id(self, response):
        css = ".js-colorspot-wrapper::attr(data-varselid)"
        return response.css(css).extract()

    def version_varsel_id(self, response):
        css = ".js-varselid-VERSION::attr(value)"
        return response.css(css).extract_first()

    def article_id(self, response):
        css = ".js-current-articleid::attr(value)"
        return response.css(css).extract_first()

    def color_name(self, response):
        css = ".js-current-color-name::attr(value)"
        return response.css(css).extract_first()

    def product_name(self, response):
        css = ".at-dv-itemName::text"
        return self.clean(response.css(css).extract())

    def product_price(self, response):
        css = ".js-webtrends-data::attr(data-content)"
        return int(float(json.loads(response.css(css).extract_first())[
            "productPrice"]) * 100)

    def currency_type(self, response):
        css = "meta[itemprop='priceCurrency']::attr(content)"
        return response.css(css).extract_first()

    def previous_price(self, response):
        css = ".js-wrong-price::text"
        return response.css(css).extract_first()

    def product_id(self, response):
        css = ".js-current-parentid::attr(value)"
        return response.css(css).extract_first()

    def product_url(self, response):
        css = "link[rel='canonical']::attr(href)"
        return response.css(css).extract_first()

    def product_description(self, response):
        css = ".details__variation__hightlights ::text"
        return self.clean(response.css(css).extract())

    def product_care(self, response):
        css = ".tmpArticleDetailTable td::text"
        return self.clean(response.css(css).extract())

    def product_brand(self, response):
        css = ".at-dv-brand::attr(content)"
        return response.css(css).extract_first()

    def product_category(self, response):
        css = ".breadcrumb a ::text"
        return response.css(css).extract()

    def product_sizes(self, response):
        css = ".at-dv-size-option::text, .at-dv-size-button::text"
        return response.css(css).extract()

    def product_pricing(self, response):
        pricing_details = {
            "price": self.product_price(response),
            "currency": self.currency_type(response)}
        prev_price = self.previous_price(response)
        if prev_price:
            pricing_details["previous_price"] = int(float(prev_price) * 100)
        return pricing_details

    def image_urls(self, response):
        css = ".imageThumb::attr(href)"
        return response.css(css).extract()

    def get_crawl_id(self):
        return f"schwab-us-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj"

    def clean(self, content):
        return [re.sub('\s+', ' ', text) for text in content if text.strip()]


class SchwabCrawler(CrawlSpider, Mixin):
    name = Mixin.name + "-crawler"
    parser = SchwabParser()
    paging_css = [".paging__btn"]
    product_css = [".product__top"]

    rules = (
        Rule(LinkExtractor(restrict_css=paging_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item"))

    def start_requests(self):
        yield Request(self.category_req_url_t, callback=self.parse_category)

    def parse_category(self, response):
        category_tree = json.loads(response.body)
        subcategory_urls = [sub["url"] for cat in category_tree for sub in cat["sCat"]]
        return self.category_requests(subcategory_urls)

    def category_requests(self, subcategory_urls):
        category_requests = []
        for url in subcategory_urls:
            category_requests.append(Request(url, callback=self.parse))
        return category_requests

    def parse_item(self, response):
        return self.parser.parse_product(response)
