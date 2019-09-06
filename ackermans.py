import json

from scrapy import Request
from w3lib.url import add_or_replace_parameters

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender, soupify


class Mixin:
    retailer = 'ackermans'
    default_brand = 'Ackermans'


class MixinZA(Mixin):
    retailer = Mixin.retailer + '-za'
    market = 'ZA'
    currency = 'ZAR'
    allowed_domains = ['ackermans.co.za', 'magento.ackermans.co.za']
    start_urls = [
        'https://www.ackermans.co.za/'
    ]
    deny = ['cellular', 'luggage-accessories', 'deals', 'toys', 'bra-guide']
    size_map_url_t = 'https://magento.ackermans.co.za/rest/default/V1/products/attributes?'
    listing_url_t = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/categoryapi/categories'
    products_page_url_t = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/searchV2?'
    image_url_t = 'https://cdn.ackermans.co.za/product-images/prod/600_600_{}.webp'
    path_url_t = 'https://www.ackermans.co.za/product'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Bearer x3leg25sl1vvruoa6vr861vgus503cfq'
    }
    pagination_request_params = {
        'search_criteria[filter_groups][2][filters][0][field]': 'category_ids',
        'search_criteria[page_size]': '20',
    }
    product_request_params = {
        'search_criteria[filter_groups][0][filters][0][field]': 'sku',
        'search_criteria[filter_groups][1][filters][0][field]': 'status',
        'search_criteria[filter_groups][1][filters][0][value]': '1',
        'search_criteria[page_size]': '1',
    }
    size_map_request_params = {
        'search_criteria[filter_groups][0][filters][0][field]': 'attribute_code',
        'search_criteria[filter_groups][0][filters][0][value]': 'size',
    }


class ParseSpider(BaseParseSpider):
    size_maps = {}

    def parse(self, response):
        raw_product = self.raw_product(response)
        product_id = self.product_id(raw_product)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        product_url = f'{response.meta["listing_url"]}/{raw_product["url_key"]}'
        self.boilerplate(garment, response, product_url)

        garment['name'] = self.product_name(raw_product)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['skus'] = self.product_skus(raw_product, response)
        garment['brand'] = self.product_brand(response)
        yield garment

    def product_skus(self, raw_product, response):
        money_strs = [raw_product['prices']['price'], self.currency]
        skus = {}

        common_sku = self.product_pricing_common(response, money_strs=money_strs)
        colour = self.detect_colour_from_name(raw_product)
        if colour:
            common_sku['colour'] = colour

        product_attributes = raw_product['custom_attributes']
        for size in product_attributes['size_ids']:
            sku = common_sku.copy()
            sku['size'] = self.size_maps[str(size)]
            sku_key = f'{sku["colour"]}_{sku["size"]}' if sku.get('colour') else f'{sku["size"]}'
            skus[sku_key] = sku

        return skus

    def raw_product(self, response):
        return json.loads(response.text)['product']['docs'][0]

    def product_id(self, raw_product):
        return raw_product['sku']

    def product_name(self, raw_product):
        return raw_product['name']

    def image_urls(self, raw_product):
        return [self.image_url_t.format(raw_product['custom_attributes']['image_name'])]

    def product_gender(self, raw_product):
        soup = soupify(raw_product['name'] + raw_product['custom_attributes']['meta_description'])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_category(self, raw_product):
        return clean(raw_product['custom_attributes']['meta_title'].split('|'))

    def raw_description(self, raw_product, **kwargs):
        return [
            raw_product['custom_attributes']['description'] +
            raw_product['custom_attributes']['meta_title'] +
            raw_product['custom_attributes']['meta_description']
        ]


class CrawlSpider(BaseCrawlSpider):
    def start_requests(self):
        size_url = add_or_replace_parameters(self.size_map_url_t, self.size_map_request_params)
        return [Request(size_url, headers=self.headers, callback=self.parse_size_maps)]

    def parse_size_maps(self, response):
        size_maps = json.loads(response.text)['items'][0]['options']
        self.parse_spider.size_maps = {size_map['value']: size_map['label'] for size_map in size_maps}
        return Request(self.listing_url_t, headers=self.headers, callback=self.parse)

    def parse(self, response):
        raw_categories = json.loads(response.text)
        meta = {'trail': self.add_trail(response)}
        yield from self.parse_categories(raw_categories, self.path_url_t, meta)

    def parse_categories(self, raw_categories, listing_url, meta, listing_id=''):
        for listing in raw_categories['children_data']:
            if listing['is_active'] and not any(deny_str in listing["url_key"] for deny_str in self.deny):
                yield from self.parse_categories(listing, f'{listing_url}/{listing["url_key"]}', meta, listing['id'])

        if not listing_id:
            return

        meta['listing_id'] = listing_id
        meta['listing_url'] = listing_url
        meta['page_number'] = 1

        product_page_url = self.pagination_request_url(meta)
        yield Request(product_page_url, headers=self.headers, callback=self.parse_pagination, meta=meta)

    def parse_pagination(self, response):
        raw_products = json.loads(response.text)['product']
        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        yield from self.product_requests(raw_products, meta.copy())

        if raw_products['data']['next_page'] and raw_products['data']['total_count']:
            response.meta['page_number'] += 1
            next_page_url = self.pagination_request_url(response.meta)
            yield Request(next_page_url, headers=self.headers,
                          callback=self.parse_pagination, meta=response.meta)

    def product_requests(self, raw_products, meta):
        for raw_product in raw_products['docs']:
            product_page_url = self.product_request_url(raw_product)
            yield Request(product_page_url, headers=self.headers,
                          callback=self.parse_spider.parse, meta=meta)

    def pagination_request_url(self, meta):
        params = {
            'search_criteria[filter_groups][2][filters][0][value]': str(meta["listing_id"]),
            'search_criteria[current_page]': str(meta["page_number"])
        }
        self.pagination_request_params.update(params)
        return add_or_replace_parameters(self.products_page_url_t, self.pagination_request_params)

    def product_request_url(self, raw_product):
        params = {
            'search_criteria[filter_groups][0][filters][0][value]': str(raw_product["sku"]),
        }
        self.product_request_params.update(params)
        return add_or_replace_parameters(self.products_page_url_t, self.product_request_params)


class ParseSpiderZA(MixinZA, ParseSpider):
    name = MixinZA.retailer + '-parse'


class CrawlSpiderZA(MixinZA, CrawlSpider):
    name = MixinZA.retailer + '-crawl'
    parse_spider = ParseSpiderZA()
