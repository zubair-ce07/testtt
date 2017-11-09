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
    raw_product_xpath = '//script[contains(text(), "__platform_data__")]/text()'
    raw_product_regex = re.compile('var __platform_data__=({.*})')

    def parse(self, response):
        raw_product = self.raw_product(response)
        product_id = self.product_id(raw_product)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['skus'] = self.skus(raw_product)
        garment['name'] = self.product_name(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['brand'] = self.product_brand(raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['image_urls'] = self.product_images(raw_product)
        garment['description'] = self.product_description(raw_product)

        return garment

    def product_id(self, raw_product):
        return raw_product['productId']

    def product_name(self, raw_product):
        return raw_product['title']

    def product_description(self, raw_product):
        return raw_product['description']

    def product_category(self, raw_product):
        return [category['name'] for category in raw_product['breadcrumb']]

    def product_care(self, raw_product):
        return raw_product['details']

    def product_brand(self, raw_product):
        return raw_product['brand'] or self.retailer

    def product_gender(self, raw_product):
        gender_text = raw_product['genderAgeGroup']

        if not gender_text:
            return 'unisex-adults'

        for gender_string, gender in self.gender_map:
            if gender_string == gender_text:
                return gender

        return 'unisex-adults'

    def product_images(self, raw_product):
        images = raw_product['imageSelector']['additionalImages'] or [raw_product['imageSelector']['defaultImage']]
        return [img['image']['src'].replace('//', '') for img in images]

    def raw_product(self, response):
        raw_product_text = clean(response.xpath(self.raw_product_xpath))[0]
        raw_product = re.findall(self.raw_product_regex, raw_product_text)
        return json.loads(raw_product[0])['pdp-data']['pdp']

    def skus(self, raw_product):
        skus = {}
        for raw_sku in raw_product['sizes']:
            sku = {}
            sku_id = raw_sku['itemId']
            sku_color = self.detect_colour(raw_product['title'])
            sku_size = self.one_size if raw_sku['size'] == "No Size" else raw_sku['size']

            price = raw_sku['price']['sale']['money']['value']
            previous_price = raw_sku['price']['regular']['money']['value']
            currency = raw_sku['price']['sale']['money']['currency']

            prices = self.product_pricing_common_new(None, [price, previous_price, currency])

            sku[sku_id] = {'color': sku_color, 'size': sku_size}
            sku[sku_id].update(prices)

            if not raw_sku['available']:
                sku[sku_id].update({'out_of_stock': True})

            skus.update(sku)

        return skus


class FanaticsCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = FanaticsParseSpider()

    menu_css = '.top-nav-dropdown-content'
    product_css = '.product-image-container'
    department_css = '.dept-card-container-black-strip'

    rules = (
        Rule(LinkExtractor(restrict_css=menu_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=department_css), callback='parse_pagination')
    )

    def parse_pagination(self, response):

        yield from self.parse(response)

        next_page = clean(response.css('[rel="next"]::attr(href)'))

        meta = {'trail': self.add_trail(response)}

        if next_page:
            next_page = next_page[0].replace('/?', '?')
            yield Request(url=next_page, callback=self.parse_pagination, meta=meta.copy())
