from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, soupify, Gender


class Mixin:
    retailer = "bonita"
    default_brand = "Bonita"


class MixinDe(Mixin):
    retailer = Mixin.retailer + "-de"
    market = "DE"

    start_urls = ["https://www.bonita.de"]
    allowed_domains = ["bonita.de"]


class ParseSpider(BaseParseSpider):
    description_css = "#productDetails .m-product-details__text li::text"
    care_css = "#material .m-product-details__text ul li::text"
    price_css = ".o-product-information__product-price"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["gender"] = self.product_gender(garment)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response, garment)

        return garment

    def product_id(self, response):
        css = ".m-product-details__text p::text"
        return response.css(css).getall()[-1].split(": ")[1]

    def product_name(self, response):
        css = ".o-product-information__product-name::text"
        return clean(response.css(css).get())

    def product_category(self, response):
        css = ".m-breadcrumb__nav ul li a::text"
        return clean(response.css(css))

    def product_gender(self, garment):
        soup = soupify(garment["category"])
        return self.gender_lookup(soup, True) or Gender.WOMEN.value

    def image_urls(self, response):
        css = ".m-zoom__image::attr(srcset)"
        images = response.css(css).getall()
        return [image.split("1x, ")[1].split("2x")[0] for image in images]

    def skus(self, response, garment):
        skus = {}
        common_sku = self.product_pricing_common(response)
        colour = self.detect_colour(garment["name"])

        if colour:
            common_sku["colour"] = colour

        for size in clean(response.css(".a-size__label::text")):
            sku = common_sku.copy()
            sku["size"] = size

            skus[f"{colour}_{size}"] = sku

        return skus


class CrawlSpider(BaseCrawlSpider):

    products_css = [".o-product-list"]
    listings_css = [
        ".o-header",
        ".m-pagination__pagination-list"
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=products_css), callback="parse_item")
    )


class ParseSpiderDe(MixinDe, ParseSpider):
    name = MixinDe.retailer + "-parse"


class CrawlSpiderDe(MixinDe, CrawlSpider):
    name = MixinDe.retailer + "-crawl"
    parse_spider = ParseSpiderDe()
