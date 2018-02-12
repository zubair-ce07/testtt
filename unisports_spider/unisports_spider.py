import json
import re

from scrapy import Request
from urllib.parse import urljoin
from w3lib.url import add_or_replace_parameter
from w3lib.url import urlencode
from .base import BaseParseSpider, BaseCrawlSpider, clean



class MixinDE:
    retailer = "unisports" + '-de'
    market = "DE"
    start_urls = ["https://www.unisport.dk/"]
    deny_urls = ["fodboldudstyr/43-fodbolde/",
                    "benskinner/1804-strompetape/",
                    "fodboldudstyr/3573-traeningsudstyr/",
                    "fodboldudstyr/299-boldpumper/",
                    "fodboldudstyr/1807-sportspleje-produkter/"]


class MixinAT:
    retailer = "unisports" + '-at'
    market = "DE"
    start_urls = ["https://www.unisportstore.at/"]
    deny_urls = ["fussballausruestung/43-fussbaelle/",
                    "schienbeinschoner/1804-sock-tape/",
                    "fussballausruestung/3573-training-equipment/",
                    "fussballausruestung/299-ballpumpen/",
                    "fussballausruestung/1807-sportpflege-produkte/"]


class MixinFR:
    retailer = "unisports" + '-fr'
    allowed_domains = ["www.unisportstore.fr"]
    market = "FR"
    start_urls = ["https://www.unisportstore.fr/"]
    deny_urls = ["equipements-de-football/43-ballons-de-football/",
                    "equipements-de-football/3573-equipement-dentrainement/",
                    "equipements-de-football/299-pompes-a-ballons/",
                    "protege-tibias/1804-bandes-de-maintien/",
                    "equipements-de-football/1807-produits-de-soin/"]


class MixinSE:
    retailer = "unisports" + '-sv'
    allowed_domains = ["www.unisportstore.se"]
    market = "SV"
    start_urls = ["https://www.unisportstore.se/"]
    deny_urls = ["fotbollsutrustning/43-fotbollar/",
                    "fotbollsutrustning/3573-traningsutrustning/",
                    "fotbollsutrustning/299-bollpumpar/",
                    "fotbollsutrustning/1807-sportskydd-rehab/",
                    "benskydd/1804-benskyddstejp/"]


class MixinFI:
    retailer = "unisports" + '-fi'
    allowed_domains = ["www.unisportstore.fi"]
    market = "FI"
    start_urls = ["https://www.unisportstore.fi/"]
    deny_urls = ["sekalaiset-tarvikkeet/43-jalkapallot/",
                    "sekalaiset-tarvikkeet/1804-sukkateippi/",
                    "sekalaiset-tarvikkeet/3573-harjoitusvalineet/",
                    "sekalaiset-tarvikkeet/299-pallopumput/",
                    "sekalaiset-tarvikkeet/1807-huoltotarvikkeet/"]


class MixinNL:
    retailer = "unisports" + '-nl'
    allowed_domains = ["www.unisportstore.nl"]
    market = "NL"
    start_urls = ["https://www.unisportstore.nl/"]
    deny_urls = ["voetbalaccessoires/43-voetballen/",
                    "voetbalaccessoires/1804-sokkentape/",
                    "voetbalaccessoires/1807-verzorgingsproducten/",
                    "voetbalaccessoires/299-balpompen/",
                    "voetbalaccessoires/3573-trainingsmateriaal/"]


class MixinNO:
    retailer = "unisports" + 'no'
    allowed_domains = ["www.unisportstore.no"]
    market = "NO"
    start_urls = ["https://www.unisportstore.no/"]
    deny_urls = ["fotballutstyr/1804-strompetape/",
                    "fotballutstyr/43-fotballer/",
                    "fotballutstyr/1807-sportspleieprodukter-medisinsk/",
                    "fotballutstyr/299-ballpumper/",
                    "fotballutstyr/3573-treningsutstyr/"]


class MixinDK:
    retailer = "unisports" + '-dk'
    allowed_domains = ["www.unisportstore.dk"]
    lang = "dk"
    market = "DA"
    start_urls = ["https://www.unisport.dk/"]
    deny_urls = ["fodboldudstyr/43-fodbolde/",
                    "benskinner/1804-strompetape/",
                    "fodboldudstyr/3573-traeningsudstyr/",
                    "fodboldudstyr/299-boldpumper/",
                    "fodboldudstyr/1807-sportspleje-produkter/"]


class UniSportParsSpider(BaseParseSpider):

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response)
        garment["gender"] = self.product_gender(response)
        return garment

    def product_id(self, response):
        return clean(response.xpath('//input[@id="id_product_id"]/@value')[0])

    def product_name(self, response):
        return clean(response.xpath('//div[@class="product-header"]//h1/text()')[0])

    def product_gender(self, response):
        product_name = self.product_name(response)
        gender = self.gender_lookup(product_name)
        return gender if gender else "men"

    def product_brand(self, response):
        xpath = '//script[contains(text(),"dataLayer")]/text()'
        return response.xpath(xpath).re_first(r'brand": \"([A-Za-z]+)')

    def raw_description(self, response):
        return clean(response.xpath('//div[@class="full-description"]//p/text()'))

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def product_category(self, response):
        return clean(response.xpath('//a[@class="crumbItems"]//span/text()'))

    def image_urls(self, response):
        return clean(response.xpath('//div[@class="product-gallery"]//a/@href'))

    def previous_price(self, response):
        raw_pprice = response.xpath('//div[@class="price-guide"]/s/text()').extract_first()
        return re.findall('[0-9,]+', raw_pprice)[0] if raw_pprice else None

    def sku_pricing(self, response):
        price = clean(response.xpath('//div/@data-product-price')[0])
        currency = clean(response.xpath('//div/@data-product-currency')[0])
        return self.product_pricing_common_new(None, money_strs=[price, self.previous_price(response), currency])

    def skus(self, response):
        sizes = clean(response.xpath('//select[@id="id_size"]/option/text()')[1:])
        sku_ids = clean(response.xpath('//select[@id="id_size"]/option/@value')[1:])
        skus = {}
        common_sku = self.sku_pricing(response)
        for size, sku_id in zip(sizes, sku_ids):
            sku = common_sku.copy()
            if size:
                sku['size'] = size.split('-')[0]
            else:
                sku["size"] = self.one_size
            skus[sku_id] = sku
        return skus


class UniSportCrawlSpider(BaseCrawlSpider):

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
                    return
                yield Request(url=urljoin(self.start_urls[0], category_url), meta={'trail': self.add_trail(response)},
                              callback=self.parse_sub_categories)

    def parse_sub_categories(self, response):
        sub_categories = response.xpath('//a[@class="nav-list facet-accordion-nav"]/@href').extract()
        for sub_category in sub_categories:
            if sub_category in self.deny_urls:
                return
            yield Request(url=urljoin(self.start_urls[0], sub_category), meta={'trail': self.add_trail(response)},
                          callback=self.raw_page)

    def raw_page(self, response):
        params = {
            "from": "0",
            "to": "120",
            "sort": "default",
            "content_type": "json"
        }
        url = response.url+"?"+urlencode(params)
        yield Request(url=url, meta={'trail': self.add_trail(response)}, callback=self.parse_pagination)

    def parse_pagination(self, response):
        max_page_num = json.loads(response.text)["max_page_number"]
        raw_urls = re.findall('"url": \"([a-z0-9-/]+)\"', response.text)
        if not raw_urls:
            return
        for url in raw_urls:
            yield Request(url=urljoin(self.start_urls[0], url), meta={'trail': self.add_trail(response)},
                          callback=self.parse_item)
        for page in range(2, int(max_page_num) + 1):
            next_page_url = add_or_replace_parameter(response.url, "page", page)
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
