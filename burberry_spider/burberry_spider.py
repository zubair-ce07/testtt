import json
from w3lib.url import add_or_replace_parameters

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender, soupify


class Mixin:
    retailer = "burberry"
    default_brand = "Burberry"


class MixinCN(Mixin):
    retailer = Mixin.retailer + "-cn"
    market = "CN"

    start_urls = ["https://cn.burberry.com"]
    allowed_domains = ["cn.burberry.com"]


class ParseSpider(BaseParseSpider):
    raw_description_css = ".accordion-tab_content ::text"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["gender"] = self.product_gender(garment)
        garment["image_urls"] = []
        garment["skus"] = {}

        garment["meta"] = {
            'requests_queue': self.color_requests(response)
        }

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = ".accordion-tab_content ::text"
        return clean(response.css(css))[-1].split(" ")[1]

    def product_name(self, response):
        css = ".product-purchase_name ::text"
        return clean(response.css(css))[0]

    def product_category(self, response):
        category = clean(response.css(".guest::attr(data-atg-category)"))[0]
        return category.split("/") if category else ""

    def product_gender(self, garment):
        soup = soupify(garment["category"], garment["name"])
        return self.gender_lookup(soup, True) or Gender.ADULTS.value

    def image_urls(self, raw_skus):
        return clean([image.get("img", {}).get("src") for image in raw_skus["hdCarousel"]])

    def color_requests(self, response):
        urls = []
        colours_css = ".product-purchase_option::attr(data-id), .guest::attr(data-product-id)"
        base_url = "https://cn.burberry.com/service/products"

        colours = clean(response.css(colours_css))
        product_url = clean(response.css(".guest::attr(data-default-url)"))[0].rsplit("-", 1)[0]
        category_id = clean(response.css(".guest::attr(data-atg-category-id)"))[0]
        csrf_token = clean(response.css(".csrf-token::attr(value)"))[0]

        for colour in colours:
            url = f"{base_url}{product_url}-p{colour}"
            add_or_replace_parameters(url, {'id': colour, 'categoryId': category_id})
            urls.append(url)

        return [Request(url, callback=self.parse_color, dont_filter=True, headers={'x-csrf-token': csrf_token})
                for url in urls]

    def parse_color(self, response):
        garment = response.meta["garment"]
        raw_skus = json.loads(response.text)
        garment["skus"].update(self.skus(raw_skus))
        garment["image_urls"] += self.image_urls(raw_skus)
        return self.next_request_or_garment(garment)

    def skus(self, raw_skus):
        skus = {}
        colour = raw_skus["dataDictionaryProductInfo"]["color"]
        money_strs = [
            raw_skus["currency"], raw_skus["dataDictionaryProductInfo"]["price"],
            raw_skus["dataDictionaryProductInfo"]["priceDiscount"]
        ]

        common_sku = self.product_pricing_common(None, money_strs=money_strs)
        common_sku["colour"] = colour

        if "size" in raw_skus["findInStore"]:
            for size in raw_skus["findInStore"]["size"]["items"]:

                sku = common_sku.copy()
                sku["size"] = size["label"]

                if size["isAvailable"] == "false":
                    sku["out of stock"] = True

                sku_id = f"{sku['colour']}_{sku['size']}" if colour else sku["size"]
                skus[sku_id] = sku

        if not skus:
            common_sku["size"] = self.one_size
            sku_id = f"{common_sku['colour']}_{common_sku['size']}" if colour else common_sku["size"]
            skus[sku_id] = common_sku

        return skus


class CrawlSpider(BaseCrawlSpider):
    products_css = [".products_container"]
    listings_css = [".header-bar_container"]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse_pagination"),
        Rule(LinkExtractor(restrict_css=products_css), callback="parse_item")
    )

    def parse_pagination(self, response):
        pagination_url_css = ".shelf::attr(data-all-products)"
        csrf_token = clean(response.css(".csrf-token::attr(value)"))[0]

        for pages in clean(response.css(pagination_url_css)):
            yield Request(response.urljoin(pages), callback="parse", headers={'x-csrf-token': csrf_token})


class ParseSpiderCN(MixinCN, ParseSpider):
    name = MixinCN.retailer + "-parse"


class CrawlSpiderCN(MixinCN, CrawlSpider):
    name = MixinCN.retailer + "-crawl"
    parse_spider = ParseSpiderCN()
