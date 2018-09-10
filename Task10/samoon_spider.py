import json

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify


class Mixin:
    retailer = 'samoon'
    allowed_domains = ['www.samoon.com']
    gender = 'women'
    merch_map = [
        ('Online Exclusive', 'ONLINE EXCLUSIVE'),
    ]
    deny_care = ['Care instructions', 'Material']


class MixinUK(Mixin):
    retailer = Mixin.retailer+"-uk"
    market = 'UK'
    start_urls = ["https://www.samoon.com/en-gb/"]


class MixinDE(Mixin):
    retailer = Mixin.retailer+"-de"
    market = 'DE'
    start_urls = ["https://www.samoon.com/de-de"]


class MixinNL(Mixin):
    retailer = Mixin.retailer+"-nl"
    market = 'NL'
    start_urls = ["https://www.samoon.com/nl-nl"]


class MixinPL(Mixin):
    retailer = Mixin.retailer+"-pl"
    market = 'PL'
    start_urls = ["https://www.samoon.com/pl-pl"]

class MixinFR(Mixin):
    retailer = Mixin.retailer+"-fr"
    market = 'FR'
    start_urls = ["https://www.samoon.com/fr-fr"]


class MixinSE(Mixin):
    retailer = Mixin.retailer+"-se"
    market = 'SE'
    start_urls = ["https://www.samoon.com/en-se"]


class SamoonParseSpider(BaseParseSpider, Mixin):
    price_css = 'div.pricing span.price *::text'
    description_css = 'div.productdescription-information-box *::text'
    care_css = 'section.pdp-material-description *::text'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["name"] = self.product_name(response)
        garment["merch_info"] = self.merch_info(response)
        garment['category'] = self.product_category(response)
        garment["image_urls"] = []

        requests = self.color_requests(response)
        if not requests:
            garment['out_of_stock'] = True
            garment.update(self.product_pricing_common(response))
            return garment

        garment["skus"] = {}
        garment['meta'] = {'requests_queue': requests}

        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta["garment"]

        requests = self.size_requests(response)
        if requests:
            garment['meta']['requests_queue'] += requests
        else:
            garment['skus'].update(self.skus(response))

        garment["image_urls"].extend(self.image_urls(response))

        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def color_requests(self, response):
        requests = clean(response.css('a.swatch-color__link::attr(href)'))
        return [response.follow(url, callback=self.parse_color, dont_filter=True)
                for url in requests]

    def size_requests(self, response):
        requests = clean(response.css('a.swatch-size__link::attr(href)'))
        return [response.follow(url, callback=self.parse_size, dont_filter=True)
                for url in requests]

    def skus(self, response):
        skus = {}
        sku = self.product_pricing_common(response)

        css = '.variation-selection::attr(data-attributes)'
        raw_sku = json.loads(clean(response.css(css))[0])

        sku["colour"] = raw_sku["color"]["displayValue"]
        size = raw_sku.get("size")
        sku["size"] = size["displayValue"] if size else self.one_size

        sku_id = f'{sku["colour"]}_{sku["size"]}'
        skus[sku_id] = sku

        return skus

    def product_id(self, response):
        return clean(response.css('.pdp-addtocart #pid::attr(value)'))[0]

    def product_name(self, response):
        css = '.product-details-container .product-name::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumb *::text'))[1:]

    def image_urls(self, response):
        selector = response.css('.gallery-thumbs-wrapper')
        urls = clean(selector.css('img::attr(src), img::attr(data-src)'))

        return [response.urljoin(src).replace("small", "large") for src in urls]

    def merch_info(self, response):
        soup = clean(response.css('.product-flag::text'))
        soup += self.product_description(response)
        soup = soupify(soup).lower()

        return [mi for m, mi in self.merch_map if m in soup]


class SamoonCrawlSpider(BaseCrawlSpider, Mixin):
    listings_css = [
        '.mainmenu__lastsubitemlist .mainmenu__showall',
        '.button-action'
    ]
    products_css = ['div[data-products-list] .product-details']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )


class SamoonUKParseSpider(SamoonParseSpider, MixinUK):
    name = MixinUK.retailer + "-parse"


class SamoonUKCrawlSpider(SamoonCrawlSpider, MixinUK):
    name = MixinUK.retailer + "-crawl"
    parse_spider = SamoonUKParseSpider()


class SamoonDEParseSpider(SamoonParseSpider, MixinDE):
    name = MixinDE.retailer + "-parse"


class SamoonDECrawlSpider(SamoonCrawlSpider, MixinDE):
    name = MixinDE.retailer + "-crawl"
    parse_spider = SamoonDEParseSpider()


class SamoonNLParseSpider(SamoonParseSpider, MixinNL):
    name = MixinNL.retailer + "-parse"


class SamoonNLCrawlSpider(SamoonCrawlSpider, MixinNL):
    name = MixinNL.retailer + "-crawl"
    parse_spider = SamoonNLParseSpider()


class SamoonPLParseSpider(SamoonParseSpider, MixinPL):
    name = MixinPL.retailer + "-parse"


class SamoonPLCrawlSpider(SamoonCrawlSpider, MixinPL):
    name = MixinPL.retailer + "-crawl"
    parse_spider = SamoonPLParseSpider()


class SamoonFRParseSpider(SamoonParseSpider, MixinFR):
    name = MixinFR.retailer + "-parse"


class SamoonFRCrawlSpider(SamoonCrawlSpider, MixinFR):
    name = MixinFR.retailer + "-crawl"
    parse_spider = SamoonFRParseSpider()


class SamoonSEParseSpider(SamoonParseSpider, MixinSE):
    name = MixinSE.retailer + "-parse"


class SamoonSECrawlSpider(SamoonCrawlSpider, MixinSE):
    name = MixinSE.retailer + "-crawl"
    parse_spider = SamoonSEParseSpider()
