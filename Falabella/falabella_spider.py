import re
import json

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'falabella-cl'
    lang = 'es'
    market = 'CL'
    allowed_domains = ['falabella.com', 'falabella.scene7.com']
    start_urls = ['http://www.falabella.com/falabella-cl/']


class FalabellaParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    image_id_re = 'Falabella/(\d+_\d)'

    gender_map = [
        ('mujer', 'women'),
        ('hombre', 'men'),
        ('niño', 'boys'),
        ('niña', 'girls'),
        ('unisex', 'unisex-adults')
    ]

    raw_product_re = 'fbra_browseMainProductConfig\s*=\s*(.*);'

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
        garment['gender'] = self.product_gender(response)
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
            colour = raw_sku.get('color', 'default')

            if colour in visited_colors:
                continue

            media_asset_id = raw_sku['mediaAssetId']
            if 'color' not in raw_sku:
                media_asset_id = raw_product['mediaAssetId']

            visited_colors.add(colour)
            url = self.image_request_url_t.format(product_id=media_asset_id)

            requests += [Request(url=url, callback=self.parse_image)]

        return requests

    def product_price(self, response, raw_sku):
        raw_pricing = sum([[p['originalPrice'], p['symbol']]
                           for p in raw_sku['price'] if p['label'] != 'CMR Puntos'], [])
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
        css = '.fb-product-information__specification__table__row-data'
        raw_description = clean(response.css('section[data-panel="longDescription"] ::text'))
        raw_description += [' '.join(clean(x.css(' ::text'))) for x in response.css(css)]

        return raw_description

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rc for rc in self.raw_description(response) if self.care_criteria_simplified(rc)]

    def product_gender(self, response):
        xpath = '//*[contains(text(), "Género")]/parent::*[th or li]//text()'

        soup = clean(response.xpath(xpath)) + [trail for trail, url in response.meta.get('trail', [])]
        soup += self.product_category(response)
        soup = ' '.join(soup).lower()

        for gender_key, gender in self.gender_map:
            if gender_key in soup:
                return gender

        return 'unisex-adults'

    def product_category(self, response):
        css = '.fb-masthead__breadcrumb__links ::text'

        return [c.replace('/ ', '') for c in clean(response.css(css))][1:]

    def raw_product(self, response):
        xpath = '//script[contains(text(), "skus")]'
        raw_product = response.xpath(xpath).re(self.raw_product_re)[0]

        return json.loads(raw_product)['state']['product']


def listing_x(categories):
    xpath_t = '//*[@data-menu-panel={panel_id}]//h4[contains(text(), "{sub_category}")]/ancestor::li[1]'

    return [xpath_t.format(panel_id=obj['id'], sub_category=sub_category)
            for obj in categories
            for sub_category in obj['categories']]


class FalabellaCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = FalabellaParseSpider()

    main_categories = [
        '//div[@data-menu-panel>=5]',
        '//div[@class="fb-hero-subnav--nav__block"]',  # sub brands
        'link[rel="next"]'
    ]

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

    product_css = '#fbra_browseProductList'

    rules = (
        Rule(LinkExtractor(restrict_xpaths=main_categories+listing_x(categories), tags=('link', 'a')),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css),
             callback='parse_item'),
    )
