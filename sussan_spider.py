import re
import json

from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request
from w3lib.url import add_or_replace_parameters

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = "sussan"
    default_brand = "Sussan"
    gender = 'women'


class MixinAU(Mixin):
    retailer = Mixin.retailer + "-au"
    market = "AU"
    start_urls = ["https://www.sussan.com.au/"]
    allowed_domains = ["www.sussan.com.au"]


class ParseSpider(BaseParseSpider):
    raw_description_css = ".short-description.std ::text, .productAttributes ::text"
    price_css = ".product-main-info .price-box ::text"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["image_urls"] = []
        garment["skus"] = {}

        garment["meta"] = {
            'requests_queue': self.color_requests(response)
        }

        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta["garment"]
        garment["skus"].update(self.skus(response))
        garment["image_urls"] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = ".product-ids::text"
        return clean(response.css(css))[0].split("-")[0]

    def product_name(self, response):
        return clean(response.css(".product-name h1::text"))[0]

    def product_category(self, response):
        return clean(response.css(".breadcrumb ::text"))[1:]

    def image_urls(self, response):
        css = ".flexslider .slides li::attr(data-thumb)"
        return clean(response.css(css))

    def color_requests(self, response):
        color_css = ".colourSwatch option::attr(value)"
        colors = clean(response.css(color_css)) or [response.url]
        return [Request(color, self.parse_color, meta=response.meta.copy(), dont_filter=True) for color in colors]

    def skus(self, response):
        skus = {}
        sizes_regex = 'label":"(.+?)"'
        sizes_css = "script:contains('attributes')"
        colours_css = ".colourSwatchWrapper option[selected='selected']::text"

        colour = clean(response.css(colours_css))
        sizes = re.findall(sizes_regex, clean(response.css(sizes_css))[0])[1:]
        common_sku = self.product_pricing_common(response)

        if colour:
            common_sku["colour"] = colour[0]

        for size in sizes:
            sku = common_sku.copy()

            if "Sold Out" in size:
                sku["out_of_stock"] = True
                size = size.split(" -")[0]

            sku["size"] = size
            skus[f"{sku['colour']}_{sku['size']}"] = sku

        if not skus:
            common_sku["size"] = self.one_size
            sku_id = f"{common_sku['colour']}_{common_sku['size']}" if colour else common_sku["size"]
            skus[sku_id] = common_sku

        return skus


class CrawlSpider(BaseCrawlSpider):
    listings_css = [".collapse.navbar-collapse.navbar-main-collapse"]

    page_size = 24

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse_pagination"),
    )

    def parse_pagination(self, response):
        product_count_css = ".pager .amount .numberOfResults::text"

        product_count = clean(response.css(product_count_css))[0].split("(")[1].split(")")[0]
        page_count = int(int(product_count)/self.page_size) + 1
        meta = self.get_meta_with_trail(response)

        return [Request(add_or_replace_parameters(response.url, {"ajax": 1, "p": page}),
                        callback=self.product_requests, meta=meta) for page in range(page_count)]

    def product_requests(self, response):
        product_css = ".product-name a::attr(href)"

        product_sel = Selector(text=json.loads(response.text)["product_list"])
        products = product_sel.css(product_css).getall()
        meta = self.get_meta_with_trail(response)

        return [Request(product_url, callback=self.parse_item, meta=meta) for product_url in products]


class ParseSpiderAU(MixinAU, ParseSpider):
    name = MixinAU.retailer + "-parse"


class CrawlSpiderAU(MixinAU, CrawlSpider):
    name = MixinAU.retailer + "-crawl"
    parse_spider = ParseSpiderAU()
