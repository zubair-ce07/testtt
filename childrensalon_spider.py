import json

import re
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'childrensalon'
    allowed_domains = ['childrensalon.com', 'petitoutlet.com']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    currency = 'GBP'

    start_urls = ['https://www.childrensalon.com', 'https://www.petitoutlet.com']

    gender_map = [
        ('Girl', 'girls'),
        ('Girls', 'girls'),
        ('Boy', 'boys'),
        ('Boys', 'boys'),
        ('Baby', 'unisex-kids')
    ]


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    currency = 'EUR'
    lang = 'de'

    gender_map = [
        ('Mädchen', 'girls'),
        ('Girls', 'girls'),
        ('Jungen', 'boys'),
        ('Boys', 'boys'),
        ('Babys', 'unisex-kids')
    ]


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    currency = 'EUR'
    lang = 'fr'

    gender_map = [
        ('Fille', 'girls'),
        ('Girls', 'girls'),
        ('Garçon', 'boys'),
        ('Boys', 'boys'),
        ('Bébé', 'unisex-kids')
    ]


class ChildrensalonParseSpider(BaseParseSpider):
    price_css = '.price-block .price-box .price::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        if "Coming Soon" in garment['category']:
            garment['out_of_stock'] = True

        if "outlet" in response.url:
            garment['outlet'] = True

        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.image_urls(response)

        garment['skus'] = self.skus(response)

        return [garment] + self.colour_requests(response)

    def raw_description(self, response):
        raw_description = clean(response.css('.description :not(strong)::text'))
        return raw_description

    def product_id(self, response):
        raw_id = response.css('.description strong::text').extract_first()
        return re.findall("\d+", raw_id)[0]

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria(rd)]

    def product_brand(self, response):
        return response.css('.product-designer ::text').extract_first()

    def product_name(self, response):
        return response.css('.product-view .product-name::text').extract_first()

    def product_category(self, response):
        return clean(response.css('.breadcrumbs ::text'))

    def product_gender(self, garment):
        raw_gender = " ".join(garment['category'] + [garment['name']])

        for gender_u, gender in self.gender_map:
            if gender_u in raw_gender:
                return gender

        return 'unisex-kids'

    def image_urls(self, response):
        return response.css('.more-views img::attr(src)').extract()

    def skus(self, response):
        skus = {}
        colour = response.css('a[class="color-swatch current-color"]::attr(title)').extract_first()
        sku_base = {'colour': colour if colour else "one_colour"}

        raw_skus = response.css('.product-options script').extract_first()
        raw_skus = re.findall("config = (.*);", raw_skus)[0]
        raw_skus = json.loads(raw_skus)
        common = self.product_pricing_common_new(response)
        size_to_code_map = {}
        for raw_sku in raw_skus["attributes"]["151"]["options"]:
            size_to_code_map[raw_sku["products"][0]] = raw_sku["label"]

        for raw_sku in size_to_code_map.keys():
            sku = sku_base.copy()
            sku["size"] = size_to_code_map[raw_sku]
            sku["price"] = common["price"] + float(raw_skus["productConfig"][raw_sku]["price"]) * 100

            if "previous_prices" in common.keys():
                sku["previous_prices"] = [
                    common["previous_prices"][0] + float(
                        (raw_skus["productConfig"][raw_sku]["oldPrice"])) * 100]

            sku["currency"] = common["currency"]

            if raw_skus["productConfig"][raw_sku]["saleable"]:
                sku["out_of_stock"] = True

            skus[sku['colour'] + "_" + sku['size']] = sku

        return skus

    def colour_requests(self, response):
        colours = response.css('a.color-swatch:not([class="color-swatch current-color"])::attr(href)').extract()
        return [Request(colour, dont_filter=True, callback=self.parse) for colour in colours]


class ChildrensalonCrawlSpider(BaseCrawlSpider):
    listings_css = [
        "ul[id='nav']",
        ".next"
    ]

    deny_r = ['/designer', '/tiny-times', '/baby/toys', '/baby/pushchairs-accessories']

    product_css = ".products-grid"

    rules = (Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'))


class ChildrensalonUKParseSpider(ChildrensalonParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class ChildrensalonUKCrawlSpider(ChildrensalonCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = ChildrensalonUKParseSpider()

    def start_requests(self):
        yield Request(
            'https://www.childrensalon.com/',
            cookies={"store": "en", "currency": "GBP"},
            callback=self.parse_outlet)

    def parse_outlet(self, response):
        return Request('https://www.petitoutlet.com', dont_filter=True)


class ChildrensalonDEParseSpider(ChildrensalonParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class ChildrensalonDECrawlSpider(ChildrensalonCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = ChildrensalonDEParseSpider()

    def start_requests(self):
        yield Request(
            'https://www.childrensalon.com/store-switcher/switch/store/code/de/?referer_url=https%3A%2F%2Fwww.childrensalon.com%2F',
            cookies={"store": "de", "currency": "EUR"},
            callback=self.parse_outlet)

    def parse_outlet(self, response):
        return Request('https://www.petitoutlet.com/store-switcher/switch/store/code/de', callback=self.parse_currency,
                       dont_filter=True)

    def parse_currency(self, response):
        return Request('https://www.petitoutlet.com/directory/currency/switch/currency/EUR', priority=1)


class ChildrensalonFRParseSpider(ChildrensalonParseSpider, MixinFR):
    name = MixinFR.retailer + '-parse'


class ChildrensalonFRCrawlSpider(ChildrensalonCrawlSpider, MixinFR):
    name = MixinFR.retailer + '-crawl'
    parse_spider = ChildrensalonFRParseSpider()

    def start_requests(self):
        yield Request(
            'https://www.childrensalon.com/store-switcher/switch/store/code/fr/?referer_url=https%3A%2F%2Fwww.childrensalon.com%2F',
            cookies={"store": "fr", "currency": "EUR"},
            callback=self.parse_outlet)

    def parse_outlet(self, response):
        return Request('https://www.petitoutlet.com/store-switcher/switch/store/code/fr', callback=self.parse_currency,
                       )

    def parse_currency(self, response):
        return Request('https://www.petitoutlet.com/directory/currency/switch/currency/EUR', priority=1, dont_filter=True)

