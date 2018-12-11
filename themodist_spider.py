from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import url_query_cleaner

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender


class Mixin:
    retailer = "themodist"
    allowed_domains = ["themodist.com"]

    default_brand = "Themodist"
    currency_map = {"UK": "GB", "EU": "DE"}


class MixinAE(Mixin):
    retailer = Mixin.retailer + "-ae"
    market = "AE"
    lang = "ar"
    start_urls = ["https://www.themodist.com/ar/"]


class MixinCN(Mixin):
    retailer = Mixin.retailer + "-cn"
    market = "CN"
    lang = "en"
    start_urls = ["https://www.themodist.com/en/"]


class MixinEU(Mixin):
    retailer = Mixin.retailer + "-eu"
    market = "EU"
    lang = "en"
    start_urls = ["https://www.themodist.com/en/"]


class MixinHK(Mixin):
    retailer = Mixin.retailer + "-hk"
    market = "HK"
    lang = "en"
    start_urls = ["https://www.themodist.com/en/"]


class MixinUK(Mixin):
    retailer = Mixin.retailer + "-uk"
    market = "UK"
    lang = "en"
    start_urls = ["https://www.themodist.com/en/"]


class MixinUS(Mixin):
    retailer = Mixin.retailer + "-us"
    market = "US"
    lang = "en"
    start_urls = ["https://www.themodist.com/en/"]


class ThemodistParseSpider(BaseParseSpider):
    description_css = ".pdp__info__content p:nth-child(1)::text"
    brand_css = ".pdp__brand ::text"
    care_css = ".pdp__info__content li:not(:last-child) ::text"
    price_css = ".price-sales::text, .price-standard::text"

    out_of_stock_text = ["Sold Out", "مُباع بالكامل"]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["image_urls"] = self.image_urls(response)
        garment["category"] = self.product_category(response)
        garment["gender"] = self.product_gender(garment)
        garment["skus"] = self.skus(response)

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = "span[itemprop='productID']::attr(data-masterid)"
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = ".pdp__name::text"
        return clean(response.css(css))[0]

    def image_urls(self, response):
        css = ".pdp__gallery__media::attr(src)"
        raw_img_urls = clean(response.css(css))
        return [url_query_cleaner(response.urljoin(url)) for url in raw_img_urls]

    def product_category(self, response):
        css = "a[id*='breadcrumb']:not(#breadcrumb1)::text"
        return clean(response.css(css))

    def product_gender(self, garment):
        soup = " ".join(garment["description"] + [garment["name"]] + garment["category"])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, response):
        skus = {}
        colour_css = ".no-sample::text"
        colour = clean(response.css(colour_css))
        size_css = ".variation-select option:not(.emptytext)::text"
        sizes = clean(response.css(size_css))

        if not sizes:
            sizes.append(self.one_size)

        for size in sizes:
            sku = self.product_pricing_common(response)
            sku["size"] = size.split("–")[0].strip()
            if colour:
                sku["colour"] = colour[0]

            if any([key for key in self.out_of_stock_text if key in size]):
                sku["out_of_stock"] = True

            sku_id = "_".join(key for key in [sku.get("colour", ""), sku["size"]] if key)
            skus[sku_id] = sku

        return skus


class ThemodistCrawlSpider(BaseCrawlSpider):
    listings_css = [".header__catmenu", ".page-next"]
    product_css = [".product__images"]

    deny_re = ["edits", "festive", "magazine", "giftcards"]

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")]

    def start_requests(self):
        cookie = self.currency_map.get(self.market) or self.market
        return [Request(url, cookies={"preferredCountry": cookie}, callback=self.parse) for url in self.start_urls]


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
