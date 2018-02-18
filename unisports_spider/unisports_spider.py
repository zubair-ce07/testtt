import json
import re

from scrapy import Request
from urllib.parse import urljoin
from w3lib.url import add_or_replace_parameter, url_query_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = "unisports"
    MERCH_INFO = [
        'limited edition'
    ]


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = "DE"

    allowed_domains = ["www.unisportstore.de"]
    start_urls = ["https://www.unisportstore.de/"]
    deny_urls = [
        "fodboldudstyr/43-fodbolde/",
        "benskinner/1804-strompetape/",
        "fodboldudstyr/3573-traeningsudstyr/",
        "fodboldudstyr/299-boldpumper/",
        "fodboldudstyr/1807-sportspleje-produkter/"
    ]


class MixinAT(Mixin):
    retailer = Mixin.retailer + '-at'
    market = "DE"

    allowed_domains = ["www.unisportstore.at"]
    start_urls = ["https://www.unisportstore.at"]
    deny_urls = [
        "fussballausruestung/43-fussbaelle/",
        "schienbeinschoner/1804-sock-tape/",
        "fussballausruestung/3573-training-equipment/",
        "fussballausruestung/299-ballpumpen/",
        "fussballausruestung/1807-sportpflege-produkte/"
    ]


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = "FR"

    allowed_domains = ["www.unisportstore.fr"]
    start_urls = ["https://www.unisportstore.fr/"]
    deny_urls = [
        "equipements-de-football/43-ballons-de-football/",
        "equipements-de-football/3573-equipement-dentrainement/",
        "equipements-de-football/299-pompes-a-ballons/",
        "protege-tibias/1804-bandes-de-maintien/",
        "equipements-de-football/1807-produits-de-soin/"
    ]


class MixinSE(Mixin):
    retailer = Mixin.retailer + '-sv'
    market = "SV"

    allowed_domains = ["www.unisportstore.se"]
    start_urls = ["https://www.unisportstore.se/"]
    deny_urls = [
        "fotbollsutrustning/43-fotbollar/",
        "fotbollsutrustning/3573-traningsutrustning/",
        "fotbollsutrustning/299-bollpumpar/",
        "fotbollsutrustning/1807-sportskydd-rehab/",
        "benskydd/1804-benskyddstejp/"
    ]


class MixinFI(Mixin):
    retailer = Mixin.retailer + '-fi'
    market = "FI"

    allowed_domains = ["www.unisportstore.fi"]
    start_urls = ["https://www.unisportstore.fi/"]
    deny_urls = [
        "sekalaiset-tarvikkeet/43-jalkapallot/",
        "sekalaiset-tarvikkeet/1804-sukkateippi/",
        "sekalaiset-tarvikkeet/3573-harjoitusvalineet/",
        "sekalaiset-tarvikkeet/299-pallopumput/",
        "sekalaiset-tarvikkeet/1807-huoltotarvikkeet/"
    ]


class MixinNL(Mixin):
    retailer = Mixin.retailer + '-nl'
    market = "NL"

    allowed_domains = ["www.unisportstore.nl"]
    start_urls = ["https://www.unisportstore.nl/"]
    deny_urls = [
        "voetbalaccessoires/43-voetballen/",
        "voetbalaccessoires/1804-sokkentape/",
        "voetbalaccessoires/1807-verzorgingsproducten/",
        "voetbalaccessoires/299-balpompen/",
        "voetbalaccessoires/3573-trainingsmateriaal/"
    ]


class MixinNO(Mixin):
    retailer = Mixin.retailer + 'no'
    market = "NO"

    allowed_domains = ["www.unisportstore.no"]
    start_urls = ["https://www.unisportstore.no/"]
    deny_urls = [
        "fotballutstyr/1804-strompetape/",
        "fotballutstyr/43-fotballer/",
        "fotballutstyr/1807-sportspleieprodukter-medisinsk/",
        "fotballutstyr/299-ballpumper/",
        "fotballutstyr/3573-treningsutstyr/"
    ]


class MixinDK(Mixin):
    retailer = Mixin.retailer + '-dk'
    market = "DK"

    allowed_domains = ["www.unisportstore.dk"]
    start_urls = ["https://www.unisport.dk/"]
    deny_urls = [
        "fodboldudstyr/43-fodbolde/",
        "benskinner/1804-strompetape/",
        "fodboldudstyr/3573-traeningsudstyr/",
        "fodboldudstyr/299-boldpumper/",
        "fodboldudstyr/1807-sportspleje-produkter/"
    ]


class UniSportParsSpider(BaseParseSpider):
    price_x = '//div/@data-product-currency | //div[@class="price price_now"]/div/text()' \
              ' | //div[@class="price-guide"]/s/text()'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["merch_info"] = self.merch_info(response)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response)
        garment["gender"] = self.product_gender(response)

        return garment

    def merch_info(self, response):
        name = self.product_name(response).lower()
        return [m for m in self.MERCH_INFO if m in name]

    def colour(self, response):
        name = self.product_name(response)
        if '-' in name:
            raw_color = name.split(' - ')[-1]
            return clean(raw_color.split(' ')[0])

        return None

    def product_id(self, response):
        return clean(response.xpath('//div[@id="prod-promotions"]/@data-product-id')[0])

    def product_name(self, response):
        product_name = clean(response.xpath('//div[@class="product-header"]//h1/text()')[0])
        return product_name.replace(self.product_brand(response), '')

    def product_gender(self, response):
        product_name = self.product_name(response)
        gender = self.gender_lookup(product_name)

        return gender if gender else Gender.MEN.value

    def product_brand(self, response):
        xpath = '//script[contains(text(),"dataLayer")]/text()'
        return response.xpath(xpath).re_first(r'brand": \"([A-Za-z]+)')

    def raw_description(self, response):
        return clean(response.xpath('//div[@class="full-description"]//p/text()'))

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def raw_category(self, response):
        category_path = []
        xpath = '//script[contains(text(),"breadcrumbData")]/text()'
        raw_category = response.xpath(xpath).re_first(r"'breadcrumbs_data': (.+),")

        for category in json.loads(raw_category):
            category_path.append(category["title"])

        return ['/'.join(category_path)] if category_path else []

    def product_category(self, response):
        category = response.xpath('//a[@class="crumbItems"]//span/text()')
        return clean(category) or self.raw_category(response)

    def image_urls(self, response):
        return clean(response.xpath('//div[@class="product-gallery"]//a/@href'))

    def skus(self, response):
        skus = {}
        colour = self.colour(response)
        size_sel = response.xpath('//select[@id="id_size"]/option')
        common_sku = self.product_pricing_common_new(response)

        if colour:
            common_sku["colour"] = colour

        for size in size_sel:
            sku_id = clean(size.xpath('./@value')[0])
            if sku_id:
                sku = common_sku.copy()
                sku["size"] = clean(size.xpath('./text()')[0]).split(' -')[0]
                skus[sku_id] = sku

        if not skus:
            sku = common_sku.copy()
            sku["size"] = self.one_size
            skus = sku

        return skus


class UniSportCrawlSpider(BaseCrawlSpider):
    url_regex = '"url": \"([a-z0-9-/]+)\"'

    def parse(self, response):
        category = response.xpath('//div[@id="offcanvas"]/@data-menu-api-url').extract_first()
        categories_url = response.urljoin(category)

        yield Request(url=categories_url, callback=self.sub_categories_urls)

    def sub_categories_urls(self, response):
        raw_category = json.loads(response.text)

        for raw_categories in raw_category["top"]:
            for categories in raw_categories["items"]:
                category_url = categories["slug"]

                if category_url in self.deny_urls:
                    continue

                yield Request(url=urljoin(self.start_urls[0], category_url), meta={'trail': self.add_trail(response)},
                              callback=self.parse_sub_categories)

    def parse_sub_categories(self, response):
        sub_categories = response.xpath('//a[@class="nav-list facet-accordion-nav"]/@href').extract()

        for sub_category in sub_categories:
            if sub_category in self.deny_urls:
                continue

            yield Request(url=response.urljoin(sub_category), meta={'trail': self.add_trail(response)},
                          callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        products_url = add_or_replace_parameter(response.url, "content_type", "json")
        products_url = add_or_replace_parameter(products_url, 'page', 1)

        yield Request(url=products_url, meta={'trail': self.add_trail(response)}, callback=self.parse_pagination)

    def parse_pagination(self, response):
        url = response.url
        max_page_num = json.loads(response.text)["max_page_number"]
        raw_urls = re.findall(self.url_regex, response.text)

        for product_url in raw_urls:
            yield Request(url=response.urljoin(product_url), meta={'trail': self.add_trail(response)},
                          callback=self.parse_item)

        current_page = url_query_parameter(url, "page")
        if int(current_page) <= max_page_num:
            next_page_url = add_or_replace_parameter(url, "page", int(current_page)+1)

            yield Request(url=next_page_url, callback=self.parse_pagination)


class UniSportParsSpiderDE(MixinDE, UniSportParsSpider):
    name = MixinDE.retailer + '-parse'


class UniSportCrawlSpiderDE(MixinDE, UniSportCrawlSpider):
    name = MixinDE.retailer + '-crawl'
    parse_spider = UniSportParsSpiderDE()


class UniSportParsSpiderAT(MixinAT, UniSportParsSpider):
    name = MixinAT.retailer + '-parse'


class UniSportCrawlSpiderAT(MixinAT, UniSportCrawlSpider):
    name = MixinAT.retailer + '-crawl'
    parse_spider = UniSportParsSpiderAT()


class UniSportParsSpiderFR(MixinFR, UniSportParsSpider):
    name = MixinFR.retailer + '-parse'


class UniSportCrawlSpiderFR(MixinFR, UniSportCrawlSpider):
    name = MixinFR.retailer + '-crawl'
    parse_spider = UniSportParsSpiderFR()


class UniSportParsSpiderSE(MixinSE, UniSportParsSpider):
    name = MixinSE.retailer + '-parse'


class UniSportCrawlSpiderSE(MixinSE, UniSportCrawlSpider):
    name = MixinSE.retailer + '-crawl'
    parse_spider = UniSportParsSpiderSE()


class UniSportParsSpiderFI(MixinFI, UniSportParsSpider):
    name = MixinFI.retailer + '-parse'


class UniSportCrawlSpiderFI(MixinFI, UniSportCrawlSpider):
    name = MixinFI.retailer + '-crawl'
    parse_spider = UniSportParsSpiderFI()


class UniSportParsSpiderNL(MixinNL, UniSportParsSpider):
    name = MixinNL.retailer + '-parse'


class UniSportCrawlSpiderNL(MixinNL, UniSportCrawlSpider):
    name = MixinNL.retailer + '-crawl'
    parse_spider = UniSportParsSpiderNL()


class UniSportParsSpiderNO(MixinNO, UniSportParsSpider):
    name = MixinNO.retailer + '-parse'


class UniSportCrawlSpiderNO(MixinNO, UniSportCrawlSpider):
    name = MixinNO.retailer + '-crawl'
    parse_spider = UniSportParsSpiderNO()


class UniSportParsSpiderDK(MixinDK, UniSportParsSpider):
    name = MixinDK.retailer + '-parse'


class UniSportCrawlSpiderDK(MixinDK, UniSportCrawlSpider):
    name = MixinDK.retailer + '-crawl'
    parse_spider = UniSportParsSpiderDK()

