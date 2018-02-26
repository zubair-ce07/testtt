import json
import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from .base import BaseCrawlSpider, BaseParseSpider, clean


class MixinUK:
    retailer = "carpisa" + '-uk'
    start_urls = ["https://www.carpisa.it/gb_en/"]
    allowed_domain = ["www.carpisa.it/gb_en"]
    market = "UK"


class MixinFR:
    retailer = "carpisa" + '-fr'
    start_urls = ["https://www.carpisa.it/fr_en/"]
    allowed_domain = ["www.carpisa.it/fr_en"]
    market = "FR"


class MixinIT:
    retailer = "carpisa" + '-it'
    start_urls = ["https://www.carpisa.it/it_it/"]
    allowed_domain = ["www.carpisa.it/it_it"]
    market = "IT"


class MixinDE:
    retailer = "carpisa" + '-de'
    start_urls = ["https://www.carpisa.it/de_en/"]
    allowed_domain = ["www.carpisa.it/de_en"]
    market = "DE"


class MixinES:
    retailer = "carpisa" + '-es'
    start_urls = ["https://www.carpisa.it/es_es/"]
    allowed_domain = ["www.carpisa.it/es_es"]
    market = "ES"


class MixinAT:
    retailer = "carpisa" + '-at'
    start_urls = ["https://www.carpisa.it/at_en/"]
    allowed_domain = ["www.carpisa.it/at_en"]
    market = "AT"


class MixinBE:
    retailer = "carpisa" + '-be'
    start_urls = ["https://www.carpisa.it/be_en/"]
    allowed_domain = ["www.carpisa.it/be_en"]
    market = "BE"


class MixinRO:
    retailer = "carpisa" + '-ro'
    retailer_currency = "EUR"
    start_urls = ["https://www.carpisa.it/ro_es/"]
    allowed_domain = ["www.carpisa.it/ro_es"]
    market = "RO"


class MixinHU:
    retailer = "carpisa" + '-hu'
    retailer_currency = "EUR"
    start_urls = ["https://www.carpisa.it/hu_es/"]
    allowed_domain = ["www.carpisa.it/hu_es"]
    market = "HU"


class MixinGR:
    retailer = "carpisa" + '-gr'
    start_urls = ["https://www.carpisa.it/gr_es/"]
    allowed_domain = ["www.carpisa.it/gr_es"]
    market = "GR"


class MixinHR:
    retailer = "carpisa" + '-hr'
    retailer_currency = "EUR"
    start_urls = ["https://www.carpisa.it/hr_es/"]
    allowed_domain = ["www.carpisa.it/hr_es"]
    market = "HR"


class CarpisaParseSpider(BaseParseSpider):
    price_css = '.special-price .price ::text, .old-price .price ::text, .regular-price span ::text'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment["image_urls"] = self.image_urls(response)
        garment["gender"] = self.product_gender(response)
        garment["skus"] = self.skus(response)

        if not garment["skus"]:
            garment.update(self.product_pricing(response))
            garment["out_of_stock"] = True

        return garment

    def product_pricing(self, response):
        price_css = '.show-for-medium p.special-price span.price ::text, .show-for-medium span.regular-price ::text'
        currency = clean(response.css('[property="product:price:currency"] ::attr(content)'))[0]
        pprice = clean(response.css('.show-for-medium p.old-price span.price ::text'))
        price = clean(response.css(price_css))[0]
        return self.product_pricing_common_new(None, money_strs=[price, pprice, currency])

    def product_id(self, response):
        return clean(response.css('.product-sku ::text'))[0]

    def product_name(self, response):
        return clean(response.css('.product-name h1 ::text'))[0]

    def product_brand(self, response):
        return 'Carpisa'

    def raw_category(self, response):
        raw_category = clean(response.css('title ::text'))[0]
        return raw_category.split('-')[-1].split('|')[0]

    def product_category(self, response):
        category = clean(response.css('span[itemprop="title"] ::text'))[1:]
        return category if category else [self.raw_category(response)]

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

    def check_availabity(self, response):
        not_available = response.css('div.product-notavaillable')
        if not_available:
            return True

    def image_urls(self, response):
        image_urls = []

        if self.check_availabity(response):
            return image_urls
        color_ids = clean(response.css('.swatches_holder')[0].css('::attr(data-swatch)'))

        if "noimage" in color_ids:
            color_ids.remove("noimage")

        for color_id in color_ids:
            image_urls += clean(response.css('figure[data-filter=\"%s\"] a ::attr(href)' % color_id))

        return image_urls

    def product_gender(self, response):
        category = '/'.join(self.product_category(response))
        gender = self.gender_lookup(category)

        return gender

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
        raw_color_ids = clean(response.css('.swatches_holder')[0].css('::attr(id)'))[1:]
        return [rcid.split('-')[-1] for rcid in raw_color_ids]

    def skus(self, response):
        skus = {}

        if self.check_availabity(response):
            return skus

        color_ids = self.colour_ids(response)
        variant_id = clean(response.css('div::attr(data-super-attr)'))[0]
        raw_product = self.raw_product(response)
        available_colors = raw_product["raw_colors"][variant_id]
        common_sku = {"size": self.one_size}

        if len(available_colors) == len(color_ids):
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

        else:
            colors = clean(response.css('.swatches_holder')[0].css('::attr(alt)'))
            for color in colors:
                sku = common_sku.copy()
                sku.update(self.product_pricing(response))
                sku["colour"] = color
                skus[color] = sku

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