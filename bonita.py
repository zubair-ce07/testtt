import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender


class Mixin:
    retailer = "bonita"


class MixinDE(Mixin):
    retailer = Mixin.retailer + "-de"
    market = "DE"
    allowed_domains = ["bonita.de"]
    start_urls = [
        "https://www.bonita.de/"
    ]

    gender = Gender.WOMEN.value
    spider_one_sizes = ['ONESIZE']


class ParseSpider(BaseParseSpider):
    price_css = ".o-product-information__product-price del::text, " \
                ".o-product-information__product-price ins::text, " \
                ".o-product-information__product-price::text"
    care_css = ".m-product-details__wash-symbols ::attr(title)"
    description_css = "#productDetails ul ::text"
    raw_brand_css = "#concreteProducts::text"
    brand_re = "brand\"\:\"(.+?)\","

    def parse(self, response):
        raw_product = self.raw_product(response)
        product_id = self.product_id(raw_product)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)
        garment['category'] = self.product_category(raw_product, product_id)
        garment['brand'] = self.product_brand(response)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response, raw_product, product_id)

        return garment

    def product_id(self, raw_product):
        return next(iter(raw_product))

    def raw_product(self, response):
        raw_product_css = "#concreteProducts::text"
        return json.loads(clean(response.css(raw_product_css))[0])

    def product_name(self, response):
        name_css = ".o-product-information__product-name::text"
        return clean(response.css(name_css))[0]

    def product_category(self, raw_product, product_id):
        return raw_product[product_id]["dimension35"].split("/")

    def image_urls(self, response):
        images_css = ".m-picture-gallery__thumb picture ::attr(data-srcset)"
        return clean(response.css(images_css))

    def skus(self, response, raw_product, product_id):
        skus = {}
        common_sku = self.product_pricing_common(response)

        alternate_color = self.detect_colour_from_name(response)
        common_sku["colour"] = raw_product[product_id]["dimension33"] or alternate_color

        for raw_size in response.css(".m-product-options li"):
            sku = common_sku.copy()
            sku["size"] = clean(raw_size.css("::attr(value)"))[0]

            if clean(raw_size.css("[disabled]")):
                sku["out_of_stock"] = True

            skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus


class CrawlSpider(BaseCrawlSpider):
    listings_css = [
        "[data-category='Navigation Desktop']",
        ".m-pagination__btn:contains('Nächste')"
    ]
    product_css = [
        ".m-product-tile__link",
        ".m-teaser-image"
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )


class ParseSpiderDE(MixinDE, ParseSpider):
    name = MixinDE.retailer + "-parse"


class CrawlSpiderDE(MixinDE, CrawlSpider):
    name = MixinDE.retailer + "-crawl"
    parse_spider = ParseSpiderDE()

