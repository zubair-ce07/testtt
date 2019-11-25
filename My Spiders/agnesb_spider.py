import json

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'agnesb'

    merch_map = [
        ('special edition', 'Special Edition'),
        ('limited edition', 'Limited Edition'),
        ('edition limitée', 'Edition limitée'),
        ('édition spéciale', 'Édition spéciale'),
        ('edición limitada', 'Edición Limitada'),
        ('edición especial', 'Edición especial'),
        ('edizione speciale', 'Edizione speciale')
    ]

    one_sizes = ['UNIQUE', 'TU']
    default_brand = 'agnès b'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    allowed_domains = ['agnesb.co.uk']
    start_urls = ['https://www.agnesb.co.uk']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    allowed_domains = ['agnesb.eu']
    start_urls = ['https://www.agnesb.eu']


class AgnesbParseSpider(BaseParseSpider):

    def parse(self, response):
        raw_product = self.raw_product(response)
        garment = self.new_unique_garment(self.product_id(raw_product))

        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = self.remove_color_from_name(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['gender'] = self.product_gender(garment)
        garment['brand'] = self.product_brand(garment)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(raw_product)
        garment['merch_info'] = self.merch_info(garment)

        return garment

    def raw_product(self, response):
        raw_product = clean(response.css('script:contains("change[\'4\']")::text'))[0].split(' = ')[1][:-1]
        return json.loads(raw_product)

    def product_id(self, raw_product):
        return raw_product['typology']['attributes']['reference_code']['value'].split('_')[0]

    def product_name(self, raw_product):
        return raw_product['common']['title']

    def product_care(self, raw_product):
        raw_care = raw_product['typology']['attributes'].get('product_care_instruction')
        care = [raw_care['value']] if raw_care else []
        raw_composition = raw_product['typology']['attributes'].get('reference_composition')
        composition = raw_composition['value'].split(',') if raw_composition else []

        return care + composition

    def product_description(self, raw_product):
        raw_description = raw_product['typology']['attributes']['product_description']['value']
        return clean(Selector(text=raw_description).css('p::text'))

    def product_gender(self, garment):
        soup = soupify([garment['url']] + garment['description'] + garment['category'])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_category(self, raw_product):
        return [raw_product['typology']['attributes']['pim_category']['value']]

    def product_brand(self, garment):
        return self.default_brand

    def image_urls(self, raw_product):
        return [v['original'] for v in raw_product['rootProduct']['common']['visuals']]

    def skus(self, raw_product):
        skus = {}

        money_strs = [
            raw_product['price'].get('baseValueWithTax'),
            raw_product['price'].get('valueWithTax'),
            raw_product['price']['currencyCode'],
        ]

        common_sku = self.product_pricing_common(None, money_strs=money_strs)

        for variant in raw_product['rootProduct']['variants']['products']:
            sku = common_sku.copy()

            if len(variant['axesValues']) > 1:
                sku['colour'] = variant['axesValues'][0].split('-')[1]
                sku['size'] = self.one_size if variant['axesValues'][1] \
                    in self.one_sizes else variant['axesValues'][1]
                sku['out_of_stock'] = not variant['hasStock']

                skus[variant['id']] = sku

        return skus

    def merch_info(self, garment):
        soup = soupify(garment['description'])
        return [m for s, m in self.merch_map if s.lower() in soup]


class AgnesbCrawlSpider(BaseCrawlSpider):
    category_css = 'nav .bullet'
    subcategory_css = '.menu-level-3 li'
    allow_re = ['/men', '/women', '/children']

    api_url = 'https://www.agnesb.co.uk/ajax.V1.php/en_GB/Rbs/Catalog/Product/'

    headers = {
        "content-type": 'application/json',
        "x-http-method-override": 'GET'
    }

    payload = {
        "sectionId": None,
        "data": {
            "webStoreId": None,
            "listId": None
        },
        "URLFormats": [
            "canonical",
            "contextual"
        ],
        "pagination": {
            "offset": 0,
            "limit": None
        }
    }

    rules = (
        Rule(LinkExtractor(restrict_css=category_css, allow=allow_re)),
        Rule(LinkExtractor(restrict_css=subcategory_css), callback='parse_pagination'),
    )

    def parse_pagination(self, response):
        raw_config = clean(response.css('[data-name="Rbs_Catalog_ProductList"] > script::text')) \
            [0].split('] = ')[1][:-1]
        config = json.loads(raw_config)
        items_count = config['pagination']['count']
        raw_section_id = clean(response.css('script:contains("__resources")::text'))[0].split(' = ')[1][:-1]

        payload_body = self.payload.copy()
        payload_body['sectionId'] = json.loads(raw_section_id)['navigationContext']['sectionId']
        payload_body['data']['webStoreId'] = config['context']['data']['webStoreId']
        payload_body['data']['listId'] = config['context']['data']['listId']
        payload_body['pagination']['limit'] = config['pagination']['limit']

        if items_count > payload_body['pagination']['limit']:
            for offset in range(0, items_count, payload_body['pagination']['limit']):
                payload_body['pagination']['offset'] += offset

                yield Request(self.api_url, method='POST', body=json.dumps(payload_body),
                              headers=self.headers, callback=self.parse_listings)

        return Request(self.api_url, method='POST', body=json.dumps(payload_body),
                       headers=self.headers, callback=self.parse_listings)

    def parse_listings(self, response):
        return [response.follow(item['common']['URL']['contextual'], self.parse_item)
                for item in json.loads(response.text)['items']]


class AgnesbUKParseSpider(MixinUK, AgnesbParseSpider):
    name = MixinUK.retailer + '-parse'


class AgnesbUKCrawlSpider(MixinUK, AgnesbCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = AgnesbUKParseSpider()


class AgnesbFRParseSpider(MixinFR, AgnesbParseSpider):
    name = MixinFR.retailer + '-parse'


class AgnesbFRCrawlSpider(MixinFR, AgnesbCrawlSpider):
    name = MixinFR.retailer + '-crawl'
    parse_spider = AgnesbFRParseSpider()
