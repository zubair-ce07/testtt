import re
import json
from scrapy.spiders import Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'fanatics-us'
    market = 'US'
    allowed_domains = ['fanatics.com']
    start_urls = ['https://www.fanatics.com/']
    gender_map = [
        ('mens', 'men'),
        ('ladies', 'women'),
        ('baby', 'unisex-kids'),
        ('kids', 'unisex-kids')
    ]


class FanaticsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    CURRENCY = '$'

    def parse(self, response):
        product_json = self.product_json(response)
        product_id = self.product_id(product_json)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = self.product_name(product_json)
        garment['care'] = self.product_care(product_json)
        garment['skus'] = self.product_skus(product_json)
        garment['brand'] = self.product_brand(product_json)
        garment['gender'] = self.product_gender(product_json)
        garment['category'] = self.product_category(product_json)
        garment['image_urls'] = self.product_images(product_json)
        garment['description'] = self.product_description(product_json)

        return self.next_request_or_garment(garment)

    def product_id(self, product_json):
        return product_json['productId']

    def product_name(self, product_json):
        return product_json['title']

    def product_description(self, product_json):
        return product_json['description']

    def product_category(self, product_json):
        return [category['name'] for category in product_json['breadcrumb']]

    def product_care(self, product_json):
        return product_json['details']

    def product_brand(self, product_json):
        return product_json['brand'] if product_json['brand'] else self.retailer

    def product_gender(self, product_json):
        gender_text = product_json['genderAgeGroup']
        if not gender_text:
            return 'unisex-adults'

        gender_text = gender_text[0].lower()

        for gender_string, gender in self.gender_map:
            if gender_text == gender_string:
                return gender

        return 'unisex-adults'

    def product_images(self, product_json):
        images = product_json['imageSelector']['additionalImages'] or [product_json['imageSelector']['defaultImage']]
        return [img['image']['src'].replace('//', '') for img in images]

    def product_skus(self, product_json):
        skus = {}
        for sku_json in product_json['sizes']:
            if sku_json['available']:
                skus.update(self.sku(sku_json, product_json['title']))

        return skus

    def sku(self, sku_json, title):
        sku = {}

        sku_id = sku_json['itemId']
        sku_size = sku_json['size']
        sku_color = self.detect_colour(title)

        pprice = sku_json['price']['regular']['money']['value'] + self.CURRENCY
        price = sku_json['price']['sale']['money']['value'] + self.CURRENCY

        prices = self.product_pricing_common_new(None, [price, pprice])

        sku[sku_id] = {'color': sku_color, 'size': self.one_size if sku_size == "No Size" else sku_size}
        sku[sku_id].update(prices)

        return sku

    def product_json(self, response):
        product_json_text = clean(response.css('.layout-row[data-trk-id="r1"] + script::text'))[0]
        product_json_text = re.findall('var __platform_data__=({.*})', product_json_text)
        return json.loads(product_json_text[0])['pdp-data']['pdp']


class FanaticsCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = FanaticsParseSpider()

    menu_css = ['.top-nav-dropdown-content']
    product_css = ['.product-image-container']
    department_css = ['.dept-card-container-black-strip']

    rules = (
        Rule(LinkExtractor(restrict_css=menu_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=department_css), callback='parse_pagination')
    )

    def parse_pagination(self, response):

        yield from self.parse(response)

        next_page = clean(response.css('[rel="next"]::attr(href)'))
        if next_page:
            next_page = next_page[0].replace('/?', '?')
            yield Request(next_page, self.parse_pagination)
