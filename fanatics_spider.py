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
        product_id = raw_product['productId']
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = raw_product['title']
        garment['care'] = raw_product['details']
        garment['description'] = raw_product['description']
        garment['brand'] = raw_product['brand'] or self.retailer
        garment['skus'] = self.skus(response, raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['image_urls'] = self.product_images(raw_product)

        return garment

    def skus(self, response, raw_product):
        skus = {}
        for raw_sku in raw_product['sizes']:
            sku = self.sku_prices(raw_sku)
            sku['colour'] = self.sku_colour(response, raw_product)
            sku['size'] = self.one_size if raw_sku['size'] == "No Size" else raw_sku['size']
            if not raw_sku['available']:
                sku['out_of_stock'] = True

            skus[raw_sku['itemId']] = sku
        return skus

    def sku_prices(self, raw_sku):
        raw_price = raw_sku['price']
        price = raw_price['sale']['money']['value']
        currency = raw_price['sale']['money']['currency']
        previous_price = raw_price['regular']['money']['value']
        return self.product_pricing_common_new(None, [price, previous_price, currency])

    def sku_colour(self, response, raw_product):
        sku_colour = response.css('.color-selector-value::text').extract_first()
        if not sku_colour:
            sku_colour = self.detect_colour(raw_product['title'])
        return sku_colour

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

    def product_category(self, raw_product):
        return [category['name'] for category in raw_product['breadcrumb']]

    def raw_product(self, response):
        raw_product_text = clean(response.xpath(self.raw_product_xpath))[0]
        raw_product = re.findall(self.raw_product_regex, raw_product_text)
        return json.loads(raw_product[0])['pdp-data']['pdp']


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
        if not next_page:
            return
        next_page = next_page[0].replace('/?', '?')
        yield Request(url=next_page, callback=self.parse_pagination, meta=meta.copy())
