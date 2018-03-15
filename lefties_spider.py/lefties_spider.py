import json

from scrapy import Request
from urllib.parse import urljoin
from scrapy.selector import Selector
from w3lib.url import add_or_replace_parameter

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = "lefties"
    images_api = "https://static.lefties.com/9/photos"
    allowed_domain = ["www.lefties.com"]
    available_categories = ["WOMEN", "MEN", "GIRLS", "BOYS"]


class MixinES(Mixin):
    retailer = Mixin.retailer + "-es"
    start_urls = ["https://www.lefties.com/es/"]
    market = "ES"
    categories_api = "https://www.lefties.com/itxrest/2/catalog/store/94009000/90009050/category?" \
                     "languageId=-5&typeCatalog=1&appId=1"
    product_api = "https://www.lefties.com/itxrest/2/catalog/store/94009000/90009050/category/0/product"


class MixinMX(Mixin):
    retailer = Mixin.retailer + "-mx"
    start_urls = ["https://www.lefties.com/mx/"]
    market = "MX"
    categories_api = "https://www.lefties.com/itxrest/2/catalog/store/94009020/90009050/category?" \
                     "languageId=-5&typeCatalog=1&appId=1"
    product_api = "https://www.lefties.com/itxrest/2/catalog/store/94009020/90009050/category/0/product"


class MixinPT(Mixin):
    retailer = Mixin.retailer + "-pt"
    start_urls = ["https://www.lefties.com/pt/"]
    market = "PT"
    categories_api = "https://www.lefties.com/itxrest/2/catalog/store/94009010/90009050/category?" \
                     "languageId=-6&typeCatalog=1&appId=1"
    product_api = "https://www.lefties.com/itxrest/2/catalog/store/94009010/90009050/category/0/product"


class MixinRU(Mixin):
    retailer = Mixin.retailer + "-ru"
    start_urls = ["https://www.lefties.com/ru/"]
    market = "RU"
    categories_api = "https://www.lefties.com/itxrest/2/catalog/store/94009022/90009050/category?" \
                     "languageId=-20&typeCatalog=1&appId=1"
    product_api = "https://www.lefties.com/itxrest/2/catalog/store/94009022/90009050/category/0/product"


class MixinQA(Mixin):
    retailer = Mixin.retailer + "-qa"
    start_urls = ["https://www.lefties.com/qa/"]
    market = "QA"
    categories_api = "https://www.lefties.com/itxrest/2/catalog/store/95009040/90009050/category?" \
                     "languageId=-1&typeCatalog=1&appId=1"
    product_api = "https://www.lefties.com/itxrest/2/catalog/store/95009040/90009050/category/0/product"


class MixinSA(Mixin):
    retailer = Mixin.retailer + "-sa"
    start_urls = ["https://www.lefties.com/sa/"]
    market = "SA"
    categories_api = "https://www.lefties.com/itxrest/2/catalog/store/95009030/90009050/category?" \
                     "languageId=-1&typeCatalog=1&appId=1"
    product_api = "https://www.lefties.com/itxrest/2/catalog/store/95009030/90009050/category/0/product"


class LeftiesParseSpider(BaseParseSpider):

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))
        if not garment:
            return

        self.boilerplate_minimal(garment, response)
        raw_product = self.raw_product(response)
        garment["name"] = self.product_name(raw_product)
        garment["brand"] = raw_product["brand"]
        garment["description"] = self.product_description(raw_product)
        garment["category"] = raw_product["offers"]["category"].split(' - ')
        garment["gender"] = self.product_gender(raw_product)
        garment['skus'] = {}
        garment['meta'] = {
            'requests_queue': self.product_details(response),
            "currency": raw_product["offers"]["priceCurrency"]
        }

        return self.next_request_or_garment(garment)

    def product_details(self, response):
        lang_id = response.xpath('//script[contains(text(),"iBrand")]/text()').re_first('LangId = (.+);')
        raw_url = f'{self.product_api}/{self.product_id(response)}/detail?appId=1'
        detail_page_url = add_or_replace_parameter(raw_url, "languageId", lang_id)

        return [Request(url=detail_page_url, callback=self.parse_details)]

    def parse_details(self, response):
        garment = response.meta["garment"]
        currency = garment["meta"]["currency"]
        raw_details = json.loads(response.text)

        if raw_details["isBuyable"] is not True:
            garment["out_of_stock"] = True

        raw_details = raw_details["detail"]
        garment["care"] = self.product_care(raw_details)
        garment["image_urls"] = self.image_urls(raw_details)
        garment["skus"] = self.skus(raw_details, currency)

        return self.next_request_or_garment(garment)

    def image_urls(self, raw_details):
        image_urls = []
        for raw_image in raw_details["colors"]:
            is_url_available = raw_image.get('image')

            if not is_url_available:
                continue
            image_url = is_url_available["url"]
            timestamp = is_url_available["timestamp"]

            for sequence_value in is_url_available["aux"]:
                code_sequence = '_'.join(["2", sequence_value, "2"])
                image_urls.append(f"{self.images_api}{image_url}_{code_sequence}.jpg?t={timestamp}")

        return image_urls

    def skus(self, raw_details, currency):
        skus = {}
        for color in raw_details["colors"]:
            sku = {"colour": color["name"]}

            for size in color["sizes"]:
                sku = sku.copy()
                if not size['isBuyable']:
                    sku["out_of_stock"] = True

                sku["size"] = "one size" if len(color["sizes"]) == 1 else size["name"]
                money_strs = [size["price"], size["oldPrice"], currency]
                sku.update(self.product_pricing_common_new(None, money_strs, is_cents=True))
                skus[size["sku"]] = sku

        return skus

    def product_id(self, response):
        raw_id = response.xpath('//script[contains(text(),"iBrand")]/text()').re_first('iParams = (.+);')
        return json.loads(raw_id)["productId"][0]

    def product_name(self, raw_product):
        name = raw_product.get("name")
        return name if name else ""

    def product_gender(self, raw_product):
        soup = raw_product["offers"]["category"]
        return self.gender_lookup(soup)

    def product_description(self, raw_product):
        raw_description = raw_product.get("description")
        return raw_description.split('. ') if raw_description else []

    def composition(self, raw_details):
        composition = []
        for raw_comp in raw_details["composition"]:
            for raw_composition in raw_comp["composition"]:
                composition.append(f"{raw_composition['percentage']}% {raw_composition['name']}")

        return composition

    def product_care(self, raw_details):
        raw_care = [care["description"] for care in raw_details["care"]] + self.composition(raw_details)
        return [pc for pc in raw_care if self.care_criteria_simplified(pc)]

    def raw_product(self, response):
        raw_product = clean(response.css('script[type="application/ld+json"] ::text'))
        if raw_product:
            return json.loads(raw_product[0])


class LeftiesCrawlSpider(BaseCrawlSpider):
    sub_categories_urls = []

    def start_requests(self):
        yield Request(url=self.categories_api, callback=self.parse_categories)

    def parse_categories(self, response):
        raw_categories = json.loads(response.text)["categories"]
        self.sub_categories(raw_categories)
        for url in self.sub_categories_urls:

            yield Request(url=urljoin(self.start_urls[0], url), meta={"trail": self.add_trail(response)},
                          callback=self.parse_sub_categories)

    def sub_categories(self, raw_categories, raw_url=''):
        temp_url = raw_url
        for category in raw_categories:

            if raw_url != '' or category['name'] in self.available_categories:
                if not category['subcategories']:
                    current_category = category["name"].replace(' ', '-')
                    self.sub_categories_urls.append(f'{raw_url}{current_category}-c{str(category["id"])}.html?')
                else:
                    raw_url += (category["name"].replace(' ', '-')).lower() + '/'
                    self.sub_categories(category['subcategories'], raw_url)
            raw_url = temp_url

    def parse_sub_categories(self, response):
        raw_text = clean(response.xpath('//noscript'))
        if raw_text:
            product_sel = Selector(text=raw_text[0])
            product_urls = clean(product_sel.css('li a ::attr(href)'))
            for product_url in product_urls:
                yield Request(url=product_url, meta={"trail": self.add_trail(response)}, callback=self.parse_item)


class LaftiesParseSpiderES(MixinES, LeftiesParseSpider):
    name = MixinES.retailer + '-parse'


class LaftiesCrawlSpiderES(MixinES, LeftiesCrawlSpider):
    name = MixinES.retailer + '-crawl'
    parse_spider = LaftiesParseSpiderES()


class LaftiesParseSpiderMX(MixinMX, LeftiesParseSpider):
    name = MixinMX.retailer + '-parse'


class LaftiesCrawlSpiderMX(MixinMX, LeftiesCrawlSpider):
    name = MixinMX.retailer + '-crawl'
    parse_spider = LaftiesParseSpiderMX()


class LaftiesParseSpiderPT(MixinPT, LeftiesParseSpider):
    name = MixinPT.retailer + '-parse'


class LaftiesCrawlSpiderPT(MixinPT, LeftiesCrawlSpider):
    name = MixinPT.retailer + '-crawl'
    parse_spider = LaftiesParseSpiderPT()


class LaftiesParseSpiderRU(MixinRU, LeftiesParseSpider):
    name = MixinRU.retailer + '-parse'


class LaftiesCrawlSpiderRU(MixinRU, LeftiesCrawlSpider):
    name = MixinRU.retailer + '-crawl'
    parse_spider = LaftiesParseSpiderRU()


class LaftiesParseSpiderQA(MixinQA, LeftiesParseSpider):
    name = MixinQA.retailer + '-parse'


class LaftiesCrawlSpiderQA(MixinQA, LeftiesCrawlSpider):
    name = MixinQA.retailer + '-crawl'
    parse_spider = LaftiesParseSpiderQA()


class LaftiesParseSpiderSA(MixinSA, LeftiesParseSpider):
    name = MixinSA.retailer + '-parse'


class LaftiesCrawlSpiderSA(MixinSA, LeftiesCrawlSpider):
    name = MixinSA.retailer + '-crawl'
    parse_spider = LaftiesParseSpiderSA()
