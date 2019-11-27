import json

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'agnesb'
    default_brand = 'Agnès B'

    merchinfo_map = [
        ('special edition', 'Special Edition'),
        ('limited edition', 'Limited Edition'),
        ('edition limitée', 'Edition limitée'),
        ('édition spéciale', 'Édition spéciale'),
        ('edición limitada', 'Edición Limitada'),
        ('edición especial', 'Edición especial'),
        ('edizione speciale', 'Edizione speciale')
    ]


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    allowed_domains = ['agnesb.co.uk']
    start_urls = ['https://www.agnesb.co.uk']
    api_url = 'https://www.agnesb.co.uk/ajax.V1.php/en_GB/Rbs/Catalog/Product/'


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    allowed_domains = ['agnesb.eu']
    start_urls = ['https://www.agnesb.eu']
    api_url = 'https://www.agnesb.eu/ajax.V1.php/fr_FR/Rbs/Catalog/Product/'


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
        css = '[data-name="Rbs_Catalog_Product"] > script::text'
        return json.loads(clean(response.css(css).re_first(r'\'] = ({.*);')))

    def product_id(self, raw_product):
        return raw_product['typology']['attributes']['reference_code']['value'].split('_')[0]

    def product_name(self, raw_product):
        return raw_product['common']['title']

    def product_care(self, raw_product):
        raw_care = raw_product['typology']['attributes']
        care = [raw_care.get('product_care_instruction', {}).get('value', '')]
        composition = raw_care.get('reference_composition', {}).get('value', '').split(',')

        return clean(care + composition)

    def product_description(self, raw_product):
        raw_description = raw_product['typology']['attributes']['product_description']['value']
        return clean(Selector(text=raw_description).css('p::text'))

    def product_gender(self, garment):
        soup = soupify([garment['url']] + garment['description'] + garment['category'])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_category(self, raw_product):
        return [raw_product['typology']['attributes']['pim_category']['value']]

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
                raw_colour, size = variant['axesValues']
                sku['colour'] = raw_colour.split('-')[1]
                sku['size'] = size
                sku['out_of_stock'] = not variant['hasStock']

                skus[variant['id']] = sku

        return skus

    def merch_info(self, garment):
        soup = soupify(garment['description'])
        return [m for s, m in self.merchinfo_map if s.lower() in soup]

def make_rules(allow_re):
    category_css = ['nav .bullet']
    subcategory_css = ['.menu-level-3 li']

    return (
        Rule(LinkExtractor(restrict_css=category_css, allow=allow_re)),
        Rule(LinkExtractor(restrict_css=subcategory_css), callback='parse_pagination'),
    )


class AgnesbCrawlSpider(BaseCrawlSpider):
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

    def parse_pagination(self, response):
        css = '[data-name="Rbs_Catalog_ProductList"] > script::text'
        config = json.loads(clean(response.css(css).re_first(r'\'] = ({.*);')))
        total_items = config['pagination']['count']
        page_size = config['pagination']['limit']

        sectionid_css = 'script:contains("sectionId")::text'
        raw_sectionid = json.loads(clean(response.css(sectionid_css).re_first(r'__change = ({.*);')))
        payload = self.payload.copy()
        payload['sectionId'] = raw_sectionid['navigationContext']['sectionId']
        payload['data']['webStoreId'] = config['context']['data']['webStoreId']
        payload['data']['listId'] = config['context']['data']['listId']
        payload['pagination']['limit'] = page_size

        for offset in range(0, total_items, page_size):
            payload['pagination']['offset'] += offset

            yield Request(self.api_url, method='POST', body=json.dumps(payload),
                          headers=self.headers, callback=self.parse_listings)

    def parse_listings(self, response):
        return [response.follow(item['common']['URL']['contextual'], self.parse_item)
                for item in json.loads(response.text)['items']]


class AgnesbUKParseSpider(MixinUK, AgnesbParseSpider):
    name = MixinUK.retailer + '-parse'


class AgnesbUKCrawlSpider(MixinUK, AgnesbCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    allow_re = ['/men', '/women', '/children']
    rules = make_rules(allow_re)
    parse_spider = AgnesbUKParseSpider()


class AgnesbFRParseSpider(MixinFR, AgnesbParseSpider):
    name = MixinFR.retailer + '-parse'


class AgnesbFRCrawlSpider(MixinFR, AgnesbCrawlSpider):
    name = MixinFR.retailer + '-crawl'
    allow_re = ['/femme', '/homme', '/enfant']
    rules = make_rules(allow_re)
    parse_spider = AgnesbFRParseSpider()
