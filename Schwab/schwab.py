import json
import re
from datetime import datetime
from urllib.parse import urlencode

from schwab.items import SchwabItem
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Mixin:
    allowed_domains = ["www.schwab.de"]
    start_urls = ["http://www.schwab.de/"]

    retailer = "schwab-gr"
    market = "GR"

    category_req_url = "https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true"
    color_req_url_t = "https://www.schwab.de/index.php?{0}"


class SchwabParser(Mixin):
    name = Mixin.retailer + "-parser"

    def parse_product(self, response):
        item = SchwabItem()
        item["uuid"] = self.product_id(response)
        item["name"] = self.product_name(response)
        item["brand"] = self.product_brand(response)
        item["category"] = self.product_category(response)
        item["crawl_id"] = self.get_crawl_id()
        item["spider_name"] = Mixin.retailer
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
        item["meta"] = {"requests": self.color_requests(response, item)}

        return self.next_request_or_item(item)

    def skus(self, response):
        skus = []
        color_css = ".js-current-color-name::attr(value)"

        product_sizes = self.clean(self.product_sizes(response))
        if not product_sizes:
            product_sizes.append("One_size")

        sku = self.product_pricing(response)
        sku["color"] = response.css(color_css).extract_first()

        for size in product_sizes:
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
        color_requests = item["meta"]["requests"]
        yield (color_requests and color_requests.pop(0)) or item

    def color_requests(self, response, item):
        colors = self.colors_varsel_id(response)
        if not colors:
            colors.append("One_Color")

        color_requests = []
        anid_css = ".js-current-articleid::attr(value)"
        version_css = ".js-varselid-VERSION::attr(value)"

        parameters = {
            "cl": "oxwarticledetails", "ajaxdetails": "adsColorChange",
            "anid": response.css(anid_css).extract_first(), "varselid[0]": "",
            "varselid[1]": response.css(version_css).extract_first()}

        for color in colors:
            parameters["varselid[2]"] = color
            url = self.color_req_url_t.format(urlencode(parameters))
            color_requests.append(Request(
                url, callback=self.parse_colors, meta={"item": item}))

        return color_requests

    def colors_varsel_id(self, response):
        css = ".js-colorspot-wrapper::attr(data-varselid)"
        return response.css(css).extract()

    def product_name(self, response):
        css = ".at-dv-itemName::text"
        return self.clean(response.css(css).extract())

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
        price_css = ".js-webtrends-data::attr(data-content)"
        currency_css = "meta[itemprop='priceCurrency']::attr(content)"
        prev_price_css = ".js-wrong-price::text"
        raw_price = json.loads(response.css(price_css).extract_first())

        pricing_details = {
            "price": int(float(raw_price["productPrice"]) * 100),
            "currency": response.css(currency_css).extract_first()}

        prev_price = response.css(prev_price_css).extract_first()
        if prev_price:
            pricing_details["previous_price"] = int(float(prev_price) * 100)

        return pricing_details

    def image_urls(self, response):
        css = ".imageThumb::attr(href)"
        return response.css(css).extract()

    def get_crawl_id(self):
        return f"schwab-us-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj"

    def clean(self, content):
        return [re.sub('\s+', ' ', text).strip() for text in content]


class SchwabCrawler(CrawlSpider, Mixin):
    name = Mixin.retailer + "-crawler"
    parser = SchwabParser()
    paging_css = [".paging__btn"]
    product_css = [".product__top"]

    rules = (
        Rule(LinkExtractor(restrict_css=paging_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item"))

    def start_requests(self):
        yield Request(self.category_req_url, callback=self.parse_category)

    def parse_category(self, response):
        category_tree = json.loads(response.body)
        subcategory_urls = [sub["url"] for cat in category_tree for sub in cat["sCat"]]

        return [Request(url, callback=self.parse) for url in subcategory_urls]

    def parse_item(self, response):
        return self.parser.parse_product(response)
