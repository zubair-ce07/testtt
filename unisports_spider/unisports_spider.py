import json
import re
import scrapy

from urllib.parse import urljoin
from w3lib.url import add_or_replace_parameter
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = "unisports"
    market = 'UK'
    urls_to_drop = ["fodboldudstyr/43-fodbolde/",
                    "benskinner/1804-strompetape/",
                    "fodboldudstyr/3573-traeningsudstyr/",
                    "fodboldudstyr/299-boldpumper/",
                    "fodboldudstyr/1807-sportspleje-produkter/"]


class MixinDe(Mixin):
    retailer = Mixin.retailer + '-de'
    base_url = "https://www.unisportstore.dk/"
    lang = "de"
    currency = "EUR"
    start_urls = ["https://www.unisportstore.dk/"]


class MixinAt(Mixin):
    retailer = Mixin.retailer + '-at'
    base_url = "https://www.unisportstore.at/"
    lang = "de"
    currency = "EUR"
    start_urls = ["https://www.unisportstore.at/"]


class MixinFr(Mixin):
    retailer = Mixin.retailer + '-fr'
    base_url = "https://www.unisportstore.fr/"
    lang = "fr"
    currency = "EUR"
    start_urls = ["https://www.unisportstore.fr/"]


class MixinSe(Mixin):
    retailer = Mixin.retailer + '-sv'
    base_url = "https://www.unisportstore.se/"
    lang = "sv"
    currency = "SEK"
    start_urls = ["https://www.unisportstore.se/"]


class MixinFi(Mixin):
    retailer = Mixin.retailer + '-fi'
    base_url = "https://www.unisportstore.fi/"
    lang = "fi"
    currency = "EUR"
    start_urls = ["https://www.unisportstore.fi/"]


class MixinDk(Mixin):
    retailer = Mixin.retailer + '-dk'
    base_url = "https://www.unisportstore.dk/"
    lang = "dk"
    currency = "DKK"
    start_urls = ["https://www.unisportstore.dk/"]


class MixinNl(Mixin):
    retailer = Mixin.retailer + '-nl'
    base_url = "https://www.unisportstore.nl/"
    lang = "nl"
    currency = "EUR"
    start_urls = ["https://www.unisportstore.nl/"]


class MixinNo(Mixin):
    retailer = Mixin.retailer + 'no'
    base_url = "https://www.unisportstore.no/"
    lang = "no"
    currency = "NOK"
    start_urls = ["https://www.unisportstore.no/"]


class UniSportParsSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"
    gender_map = [
        ('Lady', 'women'),
        ('Barn', 'unisex_Kids'),
        ('Children', 'unisex-kids'),
        ('Kids', 'unisex-kids')
    ]

    def product_id(self, response):
        return response.xpath('//input[@id="id_product_id"]/@value').extract_first()

    def product_name(self, response):
        return response.xpath('//div[@class="product-header"]//h1/text()').extract_first()

    def gender(self, response):
        product_name = self.product_name(response)
        category = re.findall("(\w+|\d+)$", product_name)[0]
        for gender_string, gender in self.gender_map:
            if gender_string == category:
                return gender
        return 'men'

    def product_brand(self, response):
        product_id_text = response.xpath('//script[contains(text(),"dataLayer")]/text()').extract_first()
        return re.findall('product_brand": \"([A-Za-z]+)', product_id_text)[0]

    def product_description(self, response):
        return response.xpath('//div[@class="full-description"]//p/text()').extract()

    def product_care(self, response):
        return "None"

    def product_category(self, response):
        return response.xpath('//a[@class="crumbItems"]//span/text()').extract_first()

    def image_urls(self, response):
        return response.xpath('//div[@class="product-gallery"]//a/@href').extract()

    def sizes(self, response):
        sizes = clean(response.xpath('//select[@id="id_size"]/option/text()').extract()[1:])
        return sizes if sizes else "size_less_product"

    def price(self, response):
        price = response.xpath('//div[@class="price price_now"]/div/text()').extract_first()
        return clean(price) if price else "None"

    def previous_price(self, response):
        previous_price = response.xpath('//div[@class="price-guide"]/s/text()').extract_first()
        return re.findall(':\s(.+)\s', previous_price)[0] if previous_price else "None"

    def sku(self, response):
        skus = []
        for size in self.sizes(response):
            skus_info = {}
            skus_info["price"] = self.price(response)
            skus_info["previous_price"] = self.previous_price(response)
            skus_info["stock"] = "available"
            skus_info["size"] = size
            skus.append(skus_info)
        return skus

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment = {}
        garment["brand"] = self.product_brand(response)
        garment["name"] = self.product_name(response)
        garment["description"] = self.product_description(response)
        garment["care"] = self.product_care(response)
        garment["category"] = self.product_category(response)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.sku(response)
        garment["gender"] = self.gender(response)
        yield garment


class UniSportCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = UniSportParsSpider()

    def parse(self, response):
        top_categories = response.xpath('//div[@id="offcanvas"]/@data-menu-api-url').extract_first()
        categories_url = response.urljoin(top_categories)
        yield scrapy.Request(url=categories_url, dont_filter=True, callback=self.categories_urls)

    def categories_urls(self, response):
        sub_cat_urls = re.findall('"slug": \"([a-z0-9-/]+)\"', response.text)
        for sub_cat_url in sub_cat_urls:
            if sub_cat_url in self.urls_to_drop:
                return
            yield scrapy.Request(url=urljoin(self.base_url, sub_cat_url), dont_filter=True,
                                 callback=self.parse_sub_categories)

    def parse_sub_categories(self, response):
        products_text_url = add_or_replace_parameter(response.url, "from", "0")
        products_text_url = add_or_replace_parameter(products_text_url, "to", "120")
        products_text_url = add_or_replace_parameter(products_text_url, "sort", "default")
        products_text_url = add_or_replace_parameter(products_text_url, "content_type", "json")
        yield scrapy.Request(url=products_text_url, dont_filter=True, callback=self.parse_next_pages)

    def parse_next_pages(self, response):
        max_page_num = json.loads(response.text)["max_page_number"]
        product_urls = re.findall('"url": \"([a-z0-9-/]+)\"', response.text)
        if not product_urls:
            return
        for product_url in product_urls:
            yield scrapy.Request(url=urljoin(self.base_url, product_url), callback=self.parse_spider.parse)
        for page in range(2, int(max_page_num)+1):
            next_page_url = add_or_replace_parameter(response.url, "page", page)
            yield scrapy.Request(url=next_page_url, callback=self.parse_next_pages)


class UniSportParsSpiderDe(MixinDe, UniSportParsSpider):
    name = MixinDe.retailer + '-parse'


class UniSportCrawlSpiderDe(MixinDe, UniSportCrawlSpider):
    name = MixinDe.retailer + '-crawl'
    parse_spider = UniSportParsSpiderDe()


class UniSportParsSpiderAt(MixinAt, UniSportParsSpider):
    name = MixinAt.retailer + '-parse'


class UniSportCrawlSpiderAt(MixinAt, UniSportCrawlSpider):
    name = MixinAt.retailer + '-crawl'
    parse_spider = UniSportParsSpiderAt()


class UniSportParsSpiderFr(MixinFr, UniSportParsSpider):
    name = MixinFr.retailer + '-parse'


class UniSportCrawlSpiderFr(MixinFr, UniSportCrawlSpider):
    name = MixinFr.retailer + '-crawl'
    parse_spider = UniSportParsSpiderFr()


class UniSportParsSpiderSe(MixinSe, UniSportParsSpider):
    name = MixinSe.retailer + '-parse'


class UniSportCrawlSpiderSe(MixinSe, UniSportCrawlSpider):
    name = MixinSe.retailer + '-crawl'
    parse_spider = UniSportParsSpiderSe()


class UniSportParsSpiderFi(MixinFi, UniSportParsSpider):
    name = MixinFi.retailer + '-parse'


class UniSportCrawlSpiderFi(MixinFi, UniSportCrawlSpider):
    name = MixinFi.retailer + '-crawl'
    parse_spider = UniSportParsSpiderFi()


class UniSportParsSpiderNl(MixinNl, UniSportParsSpider):
    name = MixinNl.retailer + '-parse'


class UniSportCrawlSpiderNL(MixinNl, UniSportCrawlSpider):
    name = MixinNl.retailer + '-crawl'
    parse_spider = UniSportParsSpiderNl()


class UniSportParsSpiderNo(MixinNo, UniSportParsSpider):
    name = MixinNo.retailer + '-parse'


class UniSportCrawlSpiderNo(MixinNo, UniSportCrawlSpider):
    name = MixinNo.retailer + '-crawl'
    parse_spider = UniSportParsSpiderNo()


class UniSportParsSpiderDk(MixinDk, UniSportParsSpider):
    name = MixinDk.retailer + '-parse'


class UniSportCrawlSpiderDk(MixinDk, UniSportCrawlSpider):
    name = MixinDk.retailer + '-crawl'
    parse_spider = UniSportParsSpiderDk()


