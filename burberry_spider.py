import json
from urllib import parse

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import url_query_cleaner

from .base import BaseCrawlSpider, BaseParseSpider, clean, soupify, Gender


class Mixin:
    retailer = "burberry"
    allowed_domains = ["cn.burberry.com"]

    default_brand = "Burberry"
    category_url_t = "https://cn.burberry.com/service/shelf{0}"
    product_url_t = "https://cn.burberry.com/service/products{0}"


class MixinCN(Mixin):
    retailer = Mixin.retailer + "-cn"
    market = "CN"
    start_urls = ["https://cn.burberry.com"]


class BurberryParseSpider(BaseParseSpider):
    description_css = ".accordion-tab_content p ::text"
    care_css = ".accordion-tab_sub-item li:not(:last-child) ::text"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["gender"] = self.product_gender(garment)
        garment["image_urls"] = []
        garment["skus"] = {}

        garment["meta"] = {"requests_queue": self.colour_requests(response)}
        return self.next_request_or_garment(garment)

    def product_name(self, response):
        css = ".product-purchase_name::text"
        return clean(response.css(css))[0]

    def product_id(self, response):
        css = "[name='product']::attr(value)"
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = "html::attr(data-atg-category)"
        category = clean(response.css(css))
        return category[0].split("/") if category else []

    def product_gender(self, garment):
        soup = soupify([garment["name"]] + garment["description"] + garment["category"])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def image_urls(self, response, raw_skus):
        return [url_query_cleaner(
            response.urljoin(img["img"]["src"])) for img in raw_skus["gallery"] if img and "img" in img]

    def colour_requests(self, response):
        css = ".product-purchase_option a::attr(href)"
        urls = clean(response.css(css)) or [parse.urlparse(response.url).path]

        token = clean(response.css(".csrf-token::attr(value)"))[0]
        headers = {"x-csrf-token": token}
        return [response.follow(
            self.product_url_t.format(url), headers=headers, callback=self.parse_colour) for url in urls]

    def parse_colour(self, response):
        raw_skus = json.loads(response.text)
        garment = response.meta['garment']
        garment["image_urls"] += self.image_urls(response, raw_skus)
        garment["skus"].update(self.skus(raw_skus))
        return self.next_request_or_garment(garment)

    def skus(self, raw_skus):
        skus = {}
        common_sku = self.product_pricing_common(None, money_strs=[raw_skus["formattedPrice"]])
        store = raw_skus["findInStore"]

        common_sku["colour"] = store["colour"]["value"] if "colour" in store \
            else self.detect_colour(raw_skus["name"])

        sizes = store["size"]["items"] if "size" in store else [{"label": self.one_size}]
        for size in sizes:
            sku = common_sku.copy()
            sku["size"] = size["label"]

            if "isAvailable" in size and not size["isAvailable"]:
                sku["out_of_stock"] = True

            sku_id = f"{sku['colour']}_{size['label']}" if sku['colour'] else size["label"]
            skus[sku_id] = sku

        return skus


class BurberryCrawlSpider(BaseCrawlSpider):
    listings_css = [".nav-level2"]
    deny_re = ["gifts"]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback="parse_pagination"),
    )

    def parse_pagination(self, response):
        categories = clean(response.css(".shelf::attr(data-url)"))
        token = clean(response.css(".csrf-token::attr(value)"))[0]
        headers = {"x-csrf-token": token}

        for url in categories:
            yield Request(self.category_url_t.format(url), meta={'trail': self.add_trail(response)},
                          headers=headers, callback=self.parse_category)

    def parse_category(self, response):
        raw_category = json.loads(response.text)
        return [response.follow(item['link'], callback=self.parse_item,
                                meta={'trail': self.add_trail(response)}) for item in raw_category]


class BurberryCNParseSpider(MixinCN, BurberryParseSpider):
    name = MixinCN.retailer + "-parse"


class BurberryCNCrawlSpider(MixinCN, BurberryCrawlSpider):
    name = MixinCN.retailer + "-crawl"
    parse_spider = BurberryCNParseSpider()
