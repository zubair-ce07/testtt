import re
import json

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request

from .base import BaseCrawlSpider, BaseParseSpider, clean


def listing_x(xpath_t, categories):
    main_categories = [
        '//div[@data-menu-panel>=5]',
        '//div[@class="fb-hero-subnav--nav__block"]',  # sub brands
        'link[rel="next"]'
    ]
    sub_categories = [xpath_t.format(panel_id=obj['id'], sub_category=sub_category)
                      for obj in categories
                      for sub_category in obj['categories']]

    return main_categories + sub_categories


class Mixin:
    retailer = 'falabella-cl'
    lang = 'es'
    market = 'CL'
    allowed_domains = ['falabella.com', 'falabella.scene7.com']
    start_urls = ['http://www.falabella.com/falabella-cl/']


class FalabellaParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    image_id_re = 'Falabella/([\d]+_[\d])'

    gender_map = [
        ('mujer', 'women'),
        ('hombre', 'men'),
        ('niño', 'boys'),
        ('niña', 'girls'),
        ('unisex', 'unisex-adults')
    ]

    raw_product_re = 'fbra_browseMainProductConfig\s=\s(.*);'

    image_url_t = 'http://falabella.scene7.com/is/image/Falabella/{image_id}'
    image_request_url_t = 'http://falabella.scene7.com/is/image/Falabella/{product_id}/?req=set,json&id=PDP'

    def parse(self, response):
        raw_product = self.raw_product(response)

        product_id = raw_product['id']
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = raw_product['displayName']
        garment['brand'] = raw_product['brand']
        garment['gender'] = self.product_gender(response, garment)
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)
        garment['skus'] = self.skus(raw_product, response)
        garment['category'] = self.product_category(response)

        garment['image_urls'] = []

        garment['meta'] = {
            'requests_queue': self.image_requests(raw_product)
        }

        return self.next_request_or_garment(garment)

    def parse_image(self, response):
        garment = response.meta.get('garment')
        garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def image_urls(self, response):
        image_ids = set(re.findall(self.image_id_re, response.text))
        return [self.image_url_t.format(image_id=image_id) for image_id in image_ids]

    def image_requests(self, raw_product):
        visited_colors = set()
        requests = []

        for raw_sku in raw_product['skus']:
            if 'color' in raw_sku and raw_sku['color'] in visited_colors:
                continue

            url = self.image_request_url_t.format(product_id=raw_sku['mediaAssetId'])

            if 'color' in raw_sku:
                visited_colors.add(raw_sku['color'])

            requests += [Request(url=url, callback=self.parse_image)]

        return requests

    def product_price(self, response, raw_sku):
        raw_pricing = sum([[p['originalPrice'], p['symbol']] for p in raw_sku['price'] if p['label'] != 'CMR Puntos'],
                          [])
        return self.product_pricing_common_new(response, money_strs=raw_pricing)

    def skus(self, raw_product, response):
        skus = {}

        for raw_sku in raw_product['skus']:
            sku = self.product_price(response, raw_sku)
            sku['size'] = raw_sku.get('size', self.one_size)

            if 'color' in raw_sku:
                sku['colour'] = raw_sku['color']

            skus[raw_sku['skuId']] = sku

        return skus

    def raw_description(self, response):
        specification_css = '.fb-product-information__specification__table__row-data'
        description = clean(response.css('section[data-panel="longDescription"] ::text'))
        specification = [' '.join(clean(x.css(' ::text'))) for x in response.css(specification_css)]
        return description + specification

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rc for rc in self.raw_description(response) if self.care_criteria_simplified(rc)]

    def product_gender(self, response, garment):
        xpath = '//section[@data-panel="longDescription"]//li[contains(text(), "Género")]/text() | ' \
                       '//th[contains(text(), "Género")]/parent::tr/td/text()'
        soup = clean(response.xpath(xpath))[0] if response.xpath(xpath) else ''
        gender = self.gender_from_soup(soup)
        return gender or self.gender_from_trail(garment)

    def gender_from_trail(self, garment):
        if not garment['trail']:
            return 'unisex-adults'

        for trail, url in garment['trail']:
            gender = self.gender_from_soup(trail)
            if gender:
                return gender

        return 'unisex-adults'

    def gender_from_soup(self, soup):
        for gender_key, gender in self.gender_map:
            if gender_key in soup.lower():
                return gender
        return None

    def product_category(self, response):
        return [cat.replace('/ ', '') for cat in clean(response.css('.fb-masthead__breadcrumb__links ::text'))
                if 'home' not in cat.lower()]

    def raw_product(self, response):
        raw_product = response.xpath('//script[contains(text(), "skus")]').re(self.raw_product_re)[0]
        return json.loads(raw_product)['state']['product']


class FalabellaCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = FalabellaParseSpider()

    categories = [
        {
            'id': '3',  # SPORTS
            'categories': ['Hombre', 'Mujer', 'Niños', 'Zapatillas']
            # Men, Women, Children, Sneakers
        },
        {
            'id': '4',  # Children
            'categories': ['Vestuario']  # Locker Room
        }
    ]

    categories_xpath_t = '//*[@data-menu-panel={panel_id}]//h4[contains(text(), "{sub_category}")]/ancestor::li[1]'

    product_css = '#fbra_browseProductList'

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listing_x(categories_xpath_t, categories), tags=('link', 'a')),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css),
             callback='parse_item'),
    )
