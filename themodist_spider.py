from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import url_query_cleaner

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender, soupify


class Mixin:
    retailer = "themodist"
    allowed_domains = ["themodist.com"]

    default_brand = "Themodist"
    currency_url_t = "https://www.themodist.com/on/demandware.store/Sites-TheModist-Site/en/" \
                     "Currency-SetSessionCountryAndCurrency?format=ajax&countryCode={}"


class MixinAE(Mixin):
    retailer = Mixin.retailer + "-ae"
    lang = "ar"
    country = market = "AE"
    start_urls = ["https://www.themodist.com/ar/"]


class MixinCN(Mixin):
    retailer = Mixin.retailer + "-cn"
    country = market = "CN"
    start_urls = ["https://www.themodist.com/en/"]


class MixinEU(Mixin):
    retailer = Mixin.retailer + "-eu"
    market = "EU"
    country = "DE"
    start_urls = ["https://www.themodist.com/en/"]


class MixinHK(Mixin):
    retailer = Mixin.retailer + "-hk"
    country = market = "HK"
    start_urls = ["https://www.themodist.com/en/"]


class MixinUK(Mixin):
    retailer = Mixin.retailer + "-uk"
    market = "UK"
    country = "GB"
    start_urls = ["https://www.themodist.com/en/"]


class MixinUS(Mixin):
    retailer = Mixin.retailer + "-us"
    country = market = "US"
    start_urls = ["https://www.themodist.com/en/"]


class ThemodistParseSpider(BaseParseSpider):
    description_css = ".pdp__info__content p:nth-child(1)::text"
    brand_css = ".pdp__brand ::text"
    care_css = ".pdp__info__content li:not(:last-child) ::text"
    price_css = ".price-sales::text, .price-standard::text"

    out_of_stock_messages = ["Sold Out", "مُباع بالكامل"]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["image_urls"] = self.image_urls(response)
        garment["gender"] = self.product_gender(garment)
        garment["skus"] = self.skus(response)

        return garment

    def product_id(self, response):
        css = "[itemprop='productID']::attr(data-masterid)"
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = ".pdp__name::text"
        return clean(response.css(css))[0]

    def image_urls(self, response):
        css = ".pdp__gallery__media::attr(src)"
        return [url_query_cleaner(response.urljoin(url)) for url in clean(response.css(css))]

    def product_category(self, response):
        css = "a[id*='breadcrumb']:not(#breadcrumb1)::text"
        return clean(response.css(css))

    def product_gender(self, garment):
        soup = soupify(garment["description"] + [garment["name"]] + garment["category"])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)

        colour = clean(response.css(".no-sample::text"))
        common_sku["colour"] = colour[0] if colour else self.detect_colour_from_name(response)

        size_css = ".variation-select option:not(.emptytext)::text"
        sizes = clean(response.css(size_css)) or [self.one_size]

        for size in sizes:
            sku = common_sku.copy()
            sku["size"] = clean(size.split("–")[0])

            if any(msg in size for msg in self.out_of_stock_messages):
                sku["out_of_stock"] = True

            sku_id = f"{sku['colour']}_{sku['size']}" if colour else sku["size"]
            skus[sku_id] = sku

        return skus


class ThemodistCrawlSpider(BaseCrawlSpider):
    listings_css = [".header__catmenu", ".page-next"]
    product_css = [".product__images"]

    deny_re = ["edits", "festive", "magazine", "giftcards"]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )

    def start_requests(self):
        yield Request(self.currency_url_t.format(self.country), callback=self.parse_cookie_request)

    def parse_cookies(self, response):
        return [response.follow(url, callback=self.parse) for url in self.start_urls]


class ThemodistAEParseSpider(MixinAE, ThemodistParseSpider):
    name = MixinAE.retailer + "-parse"


class ThemodistAECrawlSpider(MixinAE, ThemodistCrawlSpider):
    name = MixinAE.retailer + "-crawl"
    parse_spider = ThemodistAEParseSpider()


class ThemodistCNParseSpider(MixinCN, ThemodistParseSpider):
    name = MixinCN.retailer + "-parse"


class ThemodistCNCrawlSpider(MixinCN, ThemodistCrawlSpider):
    name = MixinCN.retailer + "-crawl"
    parse_spider = ThemodistCNParseSpider()


class ThemodistEUParseSpider(MixinEU, ThemodistParseSpider):
    name = MixinEU.retailer + "-parse"


class ThemodistEUCrawlSpider(MixinEU, ThemodistCrawlSpider):
    name = MixinEU.retailer + "-crawl"
    parse_spider = ThemodistEUParseSpider()


class ThemodistHKParseSpider(MixinHK, ThemodistParseSpider):
    name = MixinHK.retailer + "-parse"


class ThemodistHKCrawlSpider(MixinHK, ThemodistCrawlSpider):
    name = MixinHK.retailer + "-crawl"
    parse_spider = ThemodistHKParseSpider()


class ThemodistUKParseSpider(MixinUK, ThemodistParseSpider):
    name = MixinUK.retailer + "-parse"


class ThemodistUKCrawlSpider(MixinUK, ThemodistCrawlSpider):
    name = MixinUK.retailer + "-crawl"
    parse_spider = ThemodistUKParseSpider()


class ThemodistUSParseSpider(MixinUS, ThemodistParseSpider):
    name = MixinUS.retailer + "-parse"


class ThemodistUSCrawlSpider(MixinUS, ThemodistCrawlSpider):
    name = MixinUS.retailer + "-crawl"
    parse_spider = ThemodistUSParseSpider()
