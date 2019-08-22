import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender


class Mixin:
    retailer = "bonita"


class MixinDE(Mixin):
    market = "DE"
    retailer = Mixin.retailer + "-de"
    allowed_domains = ["bonita.de"]
    lang = "de"


def get_prices_css():
    previous_price_css = ".o-product-information__product-price del::text, "
    price_css_t1 = ".o-product-information__product-price ins::text, "
    price_css_t2 = ".o-product-information__product-price::text"
    return f"{previous_price_css}{price_css_t1}{price_css_t2}"


class BonitaParseSpider(MixinDE, BaseParseSpider):
    name = MixinDE.retailer + "-parse"
    raw_product_css = "#concreteProducts::text"

    name_css = ".o-product-information__product-name::text"
    price_css = get_prices_css()
    care_css = ".m-product-details__wash-symbols ::attr(title)"
    description_css = "#productDetails ul ::text"
    raw_brand_css = "#concreteProducts::text"
    brand_re = "brand\"\:\"(.+?)\","
    images_css = ".m-picture-gallery__thumb picture ::attr(data-srcset)"

    def parse(self, response):
        raw_product = self.raw_product(response)
        product_id = list(raw_product)[0]
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["category"] = self._product_category(raw_product)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response, raw_product)

        return garment

    def raw_product(self, response):
        return json.loads(response.css(self.raw_product_css).get())

    def product_name(self, response):
        return clean(response.css(self.name_css).get())

    def _product_category(self, raw_product):
        raw_category = raw_product[list(raw_product)[0]]["dimension35"]
        return raw_category.replace("\\", "").split("/")

    def image_urls(self, response):
        return [url for url in set(response.css(self.images_css).getall())]

    def skus(self, response, raw_product):  # Implement the pipeline, Its not there
        skus = {}
        common_sku = self.product_pricing_common(response)

        alternate_color = re.findall("in (.+)", self.product_name(response))[0]
        common_sku["colour"] = raw_product[list(raw_product)[0]]["dimension33"] or alternate_color

        for raw_size in response.css(".m-product-options li"):
            sku = common_sku.copy()
            sku["size"] = raw_size.css("::attr(value)").get()

            if raw_size.css("::attr(disabled)").get():
                sku["out_of_stock"] = True

            skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus


class BonitaCrawlSpider(MixinDE, BaseCrawlSpider):
    name = MixinDE.retailer + "-crawl"
    start_urls_with_meta = [
        ("https://www.bonita.de/", {"gender": Gender.WOMEN.value})
    ]

    parse_spider = BonitaParseSpider()

    listings_css = ["[data-category='Navigation Desktop']", ".m-pagination__btn:contains('Nächste')"]
    product_css = [".m-product-tile__link", ".m-teaser-image"]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )

