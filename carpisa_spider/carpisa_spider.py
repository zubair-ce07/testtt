import json
import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = "carpisa"
    allowed_domain = ["www.carpisa.it"]


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    start_urls = ["https://www.carpisa.it/gb_en/"]
    market = "UK"


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    start_urls = ["https://www.carpisa.it/fr_en/"]
    market = "FR"


class MixinIT(Mixin):
    retailer = Mixin.retailer + '-it'
    start_urls = ["https://www.carpisa.it/it_it/"]
    market = "IT"


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    start_urls = ["https://www.carpisa.it/de_en/"]
    market = "DE"


class MixinES(Mixin):
    retailer = Mixin.retailer + '-es'
    start_urls = ["https://www.carpisa.it/es_es/"]
    market = "ES"


class MixinAT(Mixin):
    retailer = Mixin.retailer + '-at'
    start_urls = ["https://www.carpisa.it/at_en/"]
    market = "AT"


class MixinBE(Mixin):
    retailer = Mixin.retailer + '-be'
    start_urls = ["https://www.carpisa.it/be_en/"]
    market = "BE"


class MixinRO(Mixin):
    retailer = Mixin.retailer + '-ro'
    retailer_currency = "EUR"
    start_urls = ["https://www.carpisa.it/ro_en/"]
    market = "RO"


class MixinHU(Mixin):
    retailer = Mixin.retailer + '-hu'
    retailer_currency = "EUR"
    start_urls = ["https://www.carpisa.it/hu_en/"]
    market = "HU"


class MixinGR(Mixin):
    retailer = Mixin.retailer + '-gr'
    start_urls = ["https://www.carpisa.it/gr_en/"]
    market = "GR"


class MixinHR(Mixin):
    retailer = Mixin.retailer + '-hr'
    retailer_currency = "EUR"
    start_urls = ["https://www.carpisa.it/hr_en/"]
    market = "HR"


class CarpisaParseSpider(BaseParseSpider):
    price_css = '.product-shop-wrapper .price-box span.price ::text, .price-box span.price ::text,' \
                ' .price-box span.regular-price ::text'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment["image_urls"] = self.image_urls(response)
        garment["gender"] = self.product_gender(response)
        garment["skus"] = self.skus(response)

        if not garment["skus"]:
            garment.update(self.product_pricing_common_new(response))
            garment["out_of_stock"] = True

        return garment

    def product_id(self, response):
        return clean(response.css('.product-sku ::text'))[0]

    def product_name(self, response):
        return clean(response.css('.product-name h1 ::text'))[0]

    def product_brand(self, response):
        return 'Carpisa'

    def raw_description(self, response):
        desc2 = []
        desc1 = clean(response.css('.description ::text'))
        desc2_sel = response.css('.product-collateral .attribute')

        for desc in desc2_sel:
            desc2 += [' '.join(clean(desc.css('.label ::text, .data ::text')))]

        return sum((rd.split('. ') for rd in desc1), desc2)

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def image_urls(self, response):
        return clean(response.css('a.enlarge-img ::attr(href)'))

    def product_category(self, response):
        category = clean(response.css('span[itemprop="title"] ::text'))[1:]
        return category

    def product_gender(self, response):
        category = '/'.join(self.product_category(response) + [self.product_name(response)] + [response.url])
        return self.gender_lookup(category)

    def raw_product(self, response):
        raw_product = {}
        color_price_xpath = '//div[@class="product-options base"]//script[contains(text(),"simple_product")]/text()'
        raw_color_and_price = response.xpath(color_price_xpath).extract_first()
        mappings = [("options", "colors"), ("prices", "prices"), ("images", "images")]

        for token, key in mappings:
            js = re.findall(f"{token}_(mappings|mapping).'\d+'. = (.+);", raw_color_and_price)[0]
            raw_product[f"raw_{key}"] = json.loads(js[1])

        return raw_product

    def colour_ids(self, response):
        raw_color_ids = clean(response.xpath('//div[@class="swatches_holder"]')[0].xpath('*/@id'))
        return [rcid.split('-')[-1] for rcid in raw_color_ids]

    def skus(self, response):
        skus = {}
        unavailable = bool(response.css('div.product-notavaillable'))
        if unavailable:
            return skus

        color_ids = self.colour_ids(response)
        variant_id = clean(response.css('div::attr(data-super-attr)'))[0]
        raw_product = self.raw_product(response)
        common_sku = {"size": self.one_size}

        for color_id in color_ids:
            sku_id = raw_product["raw_colors"][variant_id][color_id]["productId"]
            color = raw_product["raw_colors"][variant_id][color_id]["label"]
            price_html = raw_product["raw_prices"][sku_id]["price"]
            price_sel = Selector(text=price_html)
            sku = common_sku.copy()
            sku.update(self.product_pricing_common_new(price_sel))
            sku["colour"] = color

            if raw_product["raw_colors"][variant_id][color_id]["is_in_stock"] != 1:
                sku["out_of_stock"] = True
            skus[sku_id] = sku

        return skus


class CarpisaCrawlSpider(BaseCrawlSpider):
    listings_css = [
        'ul.level1 a',
        '.pages li a',
    ]
    product_css = '.product-image'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )


class CarpisaParseSpiderUK(MixinUK, CarpisaParseSpider):
    name = MixinUK.retailer + '-parse'


class CarpisaCrawlSpiderUK(MixinUK, CarpisaCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderUK()


class CarpisaParseSpiderFR(MixinFR, CarpisaParseSpider):
    name = MixinFR.retailer + '-parse'


class CarpisaCrawlSpiderFR(MixinFR, CarpisaCrawlSpider):
    name = MixinFR.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderFR()


class CarpisaParseSpiderIT(MixinIT, CarpisaParseSpider):
    name = MixinIT.retailer + '-parse'


class CarpisaCrawlSpiderIT(MixinIT, CarpisaCrawlSpider):
    name = MixinIT.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderIT()


class CarpisaParseSpiderDE(MixinDE, CarpisaParseSpider):
    name = MixinDE.retailer + '-parse'


class CarpisaCrawlSpiderDE(MixinDE, CarpisaCrawlSpider):
    name = MixinDE.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderDE()


class CarpisaParseSpiderES(MixinES, CarpisaParseSpider):
    name = MixinES.retailer + '-parse'


class CarpisaCrawlSpiderES(MixinES, CarpisaCrawlSpider):
    name = MixinES.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderES()


class CarpisaParseSpiderAT(MixinAT, CarpisaParseSpider):
    name = MixinAT.retailer + '-parse'


class CarpisaCrawlSpiderAT(MixinAT, CarpisaCrawlSpider):
    name = MixinAT.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderAT()


class CarpisaParseSpiderBE(MixinBE, CarpisaParseSpider):
    name = MixinBE.retailer + '-parse'


class CarpisaCrawlSpiderBE(MixinBE, CarpisaCrawlSpider):
    name = MixinBE.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderBE()


class CarpisaParseSpiderRO(MixinRO, CarpisaParseSpider):
    name = MixinRO.retailer + '-parse'


class CarpisaCrawlSpiderRO(MixinRO, CarpisaCrawlSpider):
    name = MixinRO.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderRO()


class CarpisaParseSpiderHU(MixinHU, CarpisaParseSpider):
    name = MixinHU.retailer + '-parse'


class CarpisaCrawlSpiderHU(MixinHU, CarpisaCrawlSpider):
    name = MixinHU.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderHU()


class CarpisaParseSpiderGR(MixinGR, CarpisaParseSpider):
    name = MixinGR.retailer + '-parse'


class CarpisaCrawlSpiderGR(MixinGR, CarpisaCrawlSpider):
    name = MixinGR.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderGR()


class CarpisaParseSpiderHR(MixinHR, CarpisaParseSpider):
    name = MixinHR.retailer + '-parse'


class CarpisaCrawlSpiderHR(MixinHR, CarpisaCrawlSpider):
    name = MixinHR.retailer + '-crawl'
    parse_spider = CarpisaParseSpiderHR()
