from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, soupify, Gender


class Mixin:
    retailer = "bonita"
    default_brand = "Bonita"


class MixinDE(Mixin):
    retailer = Mixin.retailer + "-de"
    market = "DE"

    start_urls = ["https://www.bonita.de"]
    allowed_domains = ["bonita.de"]


class ParseSpider(BaseParseSpider):
    raw_description_css = ".m-product-details__text ::text"
    price_css = ".o-product-information__product-price"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["gender"] = self.product_gender(garment)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response)

        return garment

    def product_id(self, response):
        css = ".m-product-details__text p::text"
        return clean(response.css(css))[-1].split(": ")[1]

    def product_name(self, response):
        css = ".o-product-information__product-name::text"
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = ".m-breadcrumb__nav ul li a::text"
        return clean(response.css(css))

    def product_gender(self, garment):
        soup = soupify(garment["category"])
        return self.gender_lookup(soup, True) or Gender.WOMEN.value

    def image_urls(self, response):
        raw_images = clean(response.css(".m-zoom__image::attr(srcset)"))
        return [image.split("1x, ")[1].split("2x")[0] for image in raw_images]

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        colour = self.detect_colour_from_name(response)

        if colour:
            common_sku["colour"] = colour

        for size_sel in response.css(".a-size__label"):
            sku = common_sku.copy()
            sku["size"] = clean(size_sel.css("::text"))[0]

            if size_sel.css(".a-size__label--disabled"):
                sku["out_of_stock"] = True

            sku_id = f"{sku['colour']}_{sku['size']}" if colour else sku["size"]
            skus[sku_id] = sku

        if not skus:
            common_sku["size"] = self.one_size
            sku_id = f"{common_sku['colour']}_{common_sku['size']}" if colour else common_sku["size"]
            skus[sku_id] = common_sku

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


class ParseSpiderDE(MixinDE, ParseSpider):
    name = MixinDE.retailer + "-parse"


class CrawlSpiderDE(MixinDE, CrawlSpider):
    name = MixinDE.retailer + "-crawl"
    parse_spider = ParseSpiderDE()
