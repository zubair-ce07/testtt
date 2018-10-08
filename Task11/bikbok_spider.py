import json
import re

from scrapy.spiders import Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'bikbok'
    allowed_domains = ['bikbok.com']
    gender = 'women'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }


class MixinNO(Mixin):
    retailer = Mixin.retailer+'-no'
    market = 'NO'
    start_urls = ["https://bikbok.com/no/"]
    form_data = '{{"CatalogNode":"{0}","MarketId":"{1}","Page":"{2}",' \
                '"ProductSearchPageId":"{3}","Language":"no"}}'
    api_request = 'https://bikbok.com/no/api/product/Post'


class BikBokParseSpider(BaseParseSpider, Mixin):

    def parse(self, response):
        raw_product = self.raw_product(response)
        sku_id = self.product_id(raw_product)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_minimal(garment, response)
        garment["name"] = self.product_name(raw_product)
        garment["category"] = self.product_category(raw_product)
        garment["description"] = self.product_description(raw_product)
        garment["care"] = self.product_care(raw_product)
        garment["brand"] = self.product_brand(raw_product)
        garment["trail"] = [response.url]
        garment["image_urls"] = []

        requests = self.color_requests(response, raw_product)
        if not requests:
            garment['out_of_stock'] = True
            money_strs = self.money_strs(raw_product)
            garment.update(self.product_pricing_common(None, money_strs=money_strs))
            return garment

        garment["skus"] = {}
        garment['meta'] = {'requests_queue': requests}

        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        raw_product = self.raw_product(response)
        garment = response.meta["garment"]

        garment["image_urls"].extend(self.image_urls(raw_product))
        garment['skus'].update(self.skus(raw_product))

        return self.next_request_or_garment(garment)

    def skus(self, raw_product):
        skus = {}
        money_strs = self.money_strs(raw_product)

        sizes = [size["Size"] for size in raw_product["Skus"]]
        for size in sizes:
            sku = self.product_pricing_common(None, money_strs=money_strs)

            sku["colour"] = raw_product["ColorFilter"]
            sku["size"] = size

            sku_id = f'{sku["colour"]}_{sku["size"]}'
            skus[sku_id] = sku

        return skus

    def color_requests(self, response, raw_product):
        requests = [request["Url"] for request in raw_product["Siblings"]]
        return [response.follow(url, callback=self.parse_color, dont_filter=True)
                for url in requests]

    def image_urls(self, raw_product):
        return [image["Url"] for image in raw_product["ProductImages"]]

    def product_id(self, raw_product):
        return raw_product["Style"]

    def product_name(self, raw_product):
        return raw_product["Name"]

    def product_category(self, raw_product):
        return raw_product["CategoryStructure"]

    def product_description(self, raw_product):
        description = raw_product["ShortDescription"]
        return clean(clean(description or '').split('\n'))

    def product_care(self, raw_product):
        return [care["Name"] for care in raw_product["ProductCare"]]

    def product_brand(self, raw_product):
        return raw_product["ProductBrand"]

    def money_strs(self, raw_product):
        prices = [raw_product["OfferedPrice"], raw_product["ListPrice"]]
        money_strs = [p["Price"] for p in prices] + [p["Currency"] for p in prices]
        return money_strs

    def raw_product(self, response):
        product_info = response.css('#main script::text').extract_first()
        raw_product = re.findall('VariantPage, (.+)\),', product_info, re.DOTALL)[0]
        raw_product = json.loads(raw_product)["product"]

        return raw_product


class BikBokCrawlSpider(BaseCrawlSpider, Mixin):
    listings_css = ['.site-nav__item.-level-1']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css),
             callback='parse_pagination'),
    )

    def parse_pagination(self, response):
        catalog_node = response.css('script').re_first('"CatalogNode":"?([\w\d]+)')
        page_id = response.css('script').re_first('"ProductSearchPageId":"?([\d]+)')
        marked_id = response.css('script').re_first('"MarketId":"?([\w\d]+)')
        total = response.css('script').re_first('"totalCount":"?([\d]+)')
        total = int(total) if total else None

        if not total:
            return

        form_data_list = [self.form_data.format(catalog_node, marked_id, page_no, page_id)
                          for page_no in range(int(total / 12))]

        requests = [Request(self.api_request, headers=MixinNO.headers, method='POST',
                            body=data, callback=self.parse_links)
                    for data in form_data_list]

        return requests

    def parse_links(self, response):
        raw_products = json.loads(response.text)["Products"]
        links = [response.follow(product["Url"], callback=self.parse_item)
                 for product in raw_products]
        return links


class DEBikBokParseSpider(BikBokParseSpider, MixinNO):
    name = MixinNO.retailer + '-parse'


class DEBikBokCrawlSpider(BikBokCrawlSpider, MixinNO):
    name = MixinNO.retailer + '-crawl'
    parse_spider = DEBikBokParseSpider()
