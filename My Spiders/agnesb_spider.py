import json

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'agnesb'
    allowed_domains = ['agnesb.co.uk', 'agnesb.eu']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = ['https://www.agnesb.co.uk']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    start_urls = ['https://www.agnesb.eu']


class AgnesbParseSpider(BaseParseSpider):
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

    def parse(self, response):
        raw_product = self.raw_product(response)
        garment = self.new_unique_garment(self.product_id(raw_product))

        if not garment:
            return

        self.boilerplate_minimal(garment, response)
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
        raw_product = clean(response.css('script').re_first(r"window.__change\['4'\] = ({.*);"))
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

        currency = raw_product['price']['currencyCode']
        previous_price = raw_product['price'].get('baseValueWithTax')
        current_price = raw_product['price'].get('valueWithTax')
        common_sku = self.product_pricing_common(None, money_strs=[previous_price, current_price, currency])

        for variant in raw_product['rootProduct']['variants']['products']:
            sku = common_sku.copy()

            if len(variant['axesValues']) > 1:
                sku['colour'] = variant['axesValues'][0].split('-')[1]
                sku['size'] = self.one_size if variant['axesValues'][1] in self.one_sizes else variant[
                    'axesValues'][1]
                sku['out_of_stock'] = variant['hasStock'] == False

                skus[variant['id']] = sku

        return skus

    def merch_info(self, garment):
        soup = soupify(garment['description'])
        return [merch for merch_str, merch in self.merch_map if merch_str.lower() in soup]


class AgnesbCrawlSpider(BaseCrawlSpider):
    category_css = 'nav .bullet'
    allow_re = ['/men', '/women', '/children']

    api_url = 'https://www.agnesb.co.uk/ajax.V1.php/en_GB/Rbs/Catalog/Product/'

    headers = {
        "content-type": 'application/json',
        "x-http-method-override": 'GET'
    }

    req_payload = {
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
        Rule(LinkExtractor(restrict_css=category_css, allow=allow_re), callback='parse_category'),
    )

    def parse_category(self, response):
        subcategory_url = response.css('.menu-level-3 li a::attr(href)').getall()
        return [response.follow(url, callback=self.parse_pagination) for url in subcategory_url]

    def parse_pagination(self, response):
        data_id = response.css('[data-name = "Rbs_Catalog_ProductList"]::attr(data-id)').get()
        raw_config = response.css('script').re_first(
            r"window.__change\["+f"'{data_id}'"+r"\] = (.*);")
        parsed_config = json.loads(raw_config)
        items_count = parsed_config['pagination']['count']

        raw_section_id = response.css('script').re_first(r"window.__change = (.*);")
        section_id = json.loads(raw_section_id)

        req_data = self.req_payload.copy()
        req_data['sectionId'] = section_id['navigationContext']['sectionId']
        req_data['data']['webStoreId'] = parsed_config['context']['data']['webStoreId']
        req_data['data']['listId'] = parsed_config['context']['data']['listId']
        req_data['pagination']['limit'] = parsed_config['pagination']['limit']

        if items_count > req_data['pagination']['limit']:
            for offset in range(0, items_count, req_data['pagination']['limit']):
                req_data['pagination']['offset'] += offset

                yield Request(self.api_url, method='POST', body=json.dumps(req_data),
                              headers=self.headers, callback=self.parse_listings)

        return Request(self.api_url, method='POST', body=json.dumps(req_data),
                       headers=self.headers, callback=self.parse_listings)

    def parse_listings(self, response):
        listings = json.loads(response.text)
        return [response.follow(item['common']['URL']['contextual'],
                                callback=self.parse_item) for item in listings['items']]

    def parse_item(self, response):
        return self.parse_spider.parse(response)


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
