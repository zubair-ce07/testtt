import json

from scrapy.spiders import Rule, Request
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'agnesb'
    default_brand = 'Agnès B'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    allowed_domains = ['agnesb.co.uk']
    start_urls = ['https://www.agnesb.co.uk']
    api_url = 'https://www.agnesb.co.uk/ajax.V1.php/en_GB/Rbs/Catalog/Product/'

    merch_info_map = [
        ('special edition', 'Special Edition'),
        ('limited edition', 'Limited Edition'),
    ]

    deny_care = ['dimension', 'length', ' x ', 'cm', 'inch']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    allowed_domains = ['agnesb.eu']
    start_urls = ['https://www.agnesb.eu']
    api_url = 'https://www.agnesb.eu/ajax.V1.php/fr_FR/Rbs/Catalog/Product/'

    merch_info_map = [
        ('edition limitée', 'Limited Edition'),
        ('édition spéciale', 'Special Edition'),
        ('edición limitada', 'Limited Edition'),
        ('edición especial', 'Special Edition'),
        ('edizione speciale', 'Special Edition')
    ]

    deny_care = ['dimension', 'length', ' x ', 'cm', 'inch', 'diamètre', 'largeur']


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
        garment['category'] = self.product_category(response)
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
        care_keys = [c['items'] for c in raw_product['typology']['visibilities']['list'] if c['key'] == 'care']
        care_keys = [c['key'] for c in care_keys[0] if 'code' not in c['key']] if care_keys else []

        care = [raw_care[c]['value'] for c in care_keys if c in raw_care]
        composition = raw_care.get('reference_composition', {}).get('value', '').split(',')

        return super().product_care(raw_product) + clean(care + composition)

    def raw_description(self, raw_product):
        raw_description = raw_product['typology']['attributes']['product_description']['value']
        return self.text_from_html(raw_description)

    def product_gender(self, garment):
        soup = soupify([garment['url']] + garment['description'])
        return self.gender_lookup(soupify(garment['category'])) or self.gender_lookup(soup) or Gender.ADULTS.value

    def product_category(self, response):
        category = [c.strip() for c in response.css('.breadcrumb li a::text').getall()][1:]
        return category + [self.raw_product(response)['typology']['attributes']['pim_category']['value']]

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
        soup = soupify(garment['description']).lower()
        return [m for s, m in self.merch_info_map if s.lower() in soup]


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
        page_size = config['pagination']['limit']

        payload = self.payload.copy()
        sectionid_css = 'script:contains("sectionId")::text'
        payload['sectionId'] = response.css(sectionid_css).re_first(r'"sectionId":(\w*),"')
        payload['data']['webStoreId'] = config['context']['data']['webStoreId']
        payload['data']['listId'] = config['context']['data']['listId']
        payload['pagination']['limit'] = page_size
        trail = self.add_trail(response)

        for offset in range(0, config['pagination']['count'], page_size):
            payload['pagination']['offset'] += offset

            yield Request(self.api_url, method='POST', body=json.dumps(payload), meta={'trail': trail},
                          headers=self.headers, callback=self.parse_listings)

    def parse_listings(self, response):
        raw_products = json.loads(response.text)['items']
        trail = self.add_trail(response)
        return [response.follow(p['common']['URL']['contextual'], self.parse_item, meta={'trail': trail})
                for p in raw_products]


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
