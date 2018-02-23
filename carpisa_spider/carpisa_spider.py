import json
import re
import html

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse
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
    start_urls = ["https://www.carpisa.it/ro_es/"]
    allowed_domain = ["www.carpisa.it/ro_es"]
    market = "RO"


class MixinHU:
    retailer = "carpisa" + '-hu'
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

        if not self.skus(response):
            garment["out_of_stock"] = True
        garment["skus"] = self.skus(response)

        return garment

    def product_id(self, response):
        return clean(response.css('.product-sku ::text')[0])

    def product_name(self, response):
        return clean(response.css('.product-name h1 ::text')[0])

    def product_brand(self, response):
        return 'Carpisa'

    def raw_category(self, response):
        raw_category = response.css('title ::text').extract_first()
        return raw_category.split('-')[-1].split('|')[0]

    def product_category(self, response):
        category = clean(response.css('span[itemprop="title"] ::text')[1:])
        return ['/'.join(category)] if category else [self.raw_category(response)]

    def raw_description(self, response):
        description = clean(response.css('.description ::text'))
        raw_description = []
        description_keys = clean(response.css('span.label ::text'))
        description_values = clean(response.css('span.data ::text'))

        for key, value in zip(description_keys, description_values):
            raw_description.append(key+value)

        return clean(sum((rd.split('.') for rd in description), raw_description))
        
    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]
    
    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def image_urls(self, response):
        image_urls = []
        raw_images = self.raw_product(response)["raw_images"]
        color_ids_sel = response.css('.swatches_holder')[0]
        color_ids = color_ids_sel.css('::attr(data-swatch)').extract()

        for color_id in color_ids:

            if color_id != "noimage":
                image_urls.append(raw_images["main"][color_id]["real"])
                image_urls.append(raw_images["more"][color_id]["real"])
                image_urls.append(raw_images["flip"][color_id]["real"])

        return image_urls if image_urls else []

    def product_gender(self, response):
        category = self.product_category(response)
        gender = self.gender_lookup(category[0])

        return gender

    def raw_product(self, response):
        raw_product = {}
        color_price_xpath = '//div[@class="product-options base"]//script[contains(text(),"simple_product")]/text()'
        raw_color_and_price = response.xpath(color_price_xpath).extract_first()

        if raw_color_and_price:
            raw_color = re.findall("options_mappings.'\d+'. = ({.+);", raw_color_and_price)[0]
            raw_price = re.findall("prices_mappings.'\d+'. = ({.+);", raw_color_and_price)[0]
            raw_image = re.findall("images_mapping.'\d+'. = ({.+);", raw_color_and_price)[0]
            raw_product["raw_colors"] = json.loads(raw_color)
            raw_product["raw_prices"] = json.loads(raw_price)
            raw_product["raw_images"] = json.loads(raw_image)

            return raw_product

    def colour_ids(self, response):
        color_ids = []
        color_ids_sel = response.css('.swatches_holder')[0]
        raw_color_ids = color_ids_sel.css('::attr(id)').extract()[1:]

        for raw_color_id in raw_color_ids:
            color_ids.append(raw_color_id.split('-')[-1])

        return color_ids

    def product_not_exist(self, response):
        product_css = 'div[data-append="product-availlable"] ::text'
        product = clean(response.css(product_css)[-1])

        if product == "Product not availlable":
            return True

    def skus(self, response):
        skus = {}

        if self.product_not_exist(response):
            return skus

        variant_id = clean(response.css('div::attr(data-super-attr)')[0])
        raw_color = self.raw_product(response)["raw_colors"]
        raw_price = self.raw_product(response)["raw_prices"]

        for color_id in self.colour_ids(response):
            sku_id = raw_color[variant_id][color_id]["productId"]
            color = raw_color[variant_id][color_id]["label"]
            price_html = raw_price[sku_id]["price"]
            new_response = HtmlResponse(url="", body=html.unescape(price_html), encoding='utf-8')
            new_response_sel = Selector(text=new_response.text)
            common_sku = self.product_pricing_common_new(new_response_sel)
            common_sku["colour"] = color
            common_sku["size"] = self.one_size

            if raw_color[variant_id][color_id]["is_in_stock"] != 1:
                common_sku["out_of_stock"] = True
            skus[sku_id] = common_sku

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
