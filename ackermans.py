import json
from urllib.parse import urlencode

from scrapy import Request

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender, soupify


class Mixin:
    retailer = 'ackermans'
    default_brand = "Ackermans"


class MixinZA(Mixin):
    retailer = Mixin.retailer + '-za'
    market = 'ZA'
    allowed_domains = ['ackermans.co.za', 'magento.ackermans.co.za']
    start_urls = [
        'https://www.ackermans.co.za/'
    ]
    deny = ['cellular', 'luggage-accessories', 'deals', 'toys', 'bra-guide']
    size_map_url_t = 'https://magento.ackermans.co.za/rest/default/V1/products/attributes?'
    listing_url_t = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/categoryapi/categories'
    products_page_url_t = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/searchV2?'
    image_url_t = 'https://cdn.ackermans.co.za/product-images/prod/600_600_{}.webp'
    path_url_t = 'https://www.ackermans.co.za/products'

    size_maps = []
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.ackermans.co.za/',
        'Origin': 'https://www.ackermans.co.za',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3770.142 Safari/537.36',
        'Authorization': 'Bearer x3leg25sl1vvruoa6vr861vgus503cfq',
    }
    pagination_request_params = [
        ['search_criteria[filter_groups][2][filters][0][value]', ''],
        ['search_criteria[current_page]', ''],
        ['search_criteria[filter_groups][0][filters][0][field]', 'status'],
        ['search_criteria[filter_groups][0][filters][0][value]', '1'],
        ['search_criteria[filter_groups][1][filters][0][field]', 'visibility'],
        ['search_criteria[filter_groups][1][filters][0][value]', '4'],
        ['search_criteria[filter_groups][2][filters][0][field]', 'category_ids'],
        ['search_criteria[page_size]', '20'],
        ['tracker', 'a2zxlqwzj6-1567316733-1'],
    ]
    product_request_params = [
        ['search_criteria[filter_groups][0][filters][0][value]', ''],
        ['search_criteria[filter_groups][0][filters][0][field]', 'sku'],
        ['search_criteria[filter_groups][1][filters][0][field]', 'status'],
        ['search_criteria[filter_groups][1][filters][0][value]', '1'],
        ['search_criteria[page_size]', '1'],
        ['search_criteria[current_page]', '1'],
        ['tracker', 'ormxxa2vwxm-1567410631-1'],
    ]
    color_map_request_params = (
        ('search_criteria[filter_groups][0][filters][0][condition_type]', 'in'),
        ('search_criteria[filter_groups][0][filters][0][field]', 'attribute_code'),
        ('search_criteria[filter_groups][0][filters][0][value]', 'size'),
        ('tracker', 'elkc0x97qp9-1567485069-1'),
    )


class ParseSpider(BaseParseSpider):
    def parse(self, response):
        raw_product = self.raw_product(response)
        product_id = self.product_id(raw_product)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_minimal(garment, response)

        garment['name'] = self.product_name(raw_product)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['skus'] = self.product_skus(raw_product, response)
        garment['brand'] = self.product_brand(response)
        garment['url'] = self.product_url(response, raw_product)
        garment['trail'] = self.product_trail(response)
        yield garment

    def product_skus(self, raw_product, response):
        money_strs = [raw_product['prices']['price'], 'ZAR']
        size_maps = response.meta['size_maps']
        skus = {}

        common_sku = self.product_pricing_common(response, money_strs=money_strs)
        colour = self.detect_colour_from_name(raw_product)
        if colour:
            common_sku['colour'] = colour

        product_attributes = raw_product['custom_attributes']

        for size in product_attributes['size_ids']:
            sku = common_sku.copy()
            sku['size'] = size_maps[str(size)]
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

    def product_description(self, raw_product):
        return clean(raw_product['custom_attributes']['meta_description'].split(','))

    def product_care(self, raw_product):
        description = self.product_description(raw_product)
        return [raw_Care for raw_Care in description
                if self.care_criteria(raw_Care)]

    def product_url(self, response, raw_product):
        url = f'{response.meta["listing_url"]}/{raw_product["url_key"]}'
        return url.replace('products', 'product')

    def product_trail(self, response):
        return self.add_trail(response)


class CrawlSpider(BaseCrawlSpider):
    def start_requests(self):
        params = urlencode(self.color_map_request_params)
        return [Request(f'{self.size_map_url_t}{params}', method='GET', headers=self.headers,
                        callback=self.parse_size_maps)]

    def parse_size_maps(self, response):
        size_maps = json.loads(response.text)['items'][0]['options']
        self.size_maps = {size_map['value']: size_map['label'] for size_map in size_maps if size_map['value']}
        return Request(self.listing_url_t, method='GET', headers=self.headers, callback=self.parse_listings)

    def parse_listings(self, response):
        raw_json = json.loads(response.text)
        meta = {
            'trail': self.add_trail(response)
        }
        yield from self.parse_listings_url(raw_json, self.path_url_t, meta)

    def parse_listings_url(self, raw_json, listing_url, meta, listing_id=''):
        for listing in raw_json['children_data']:
            if listing['is_active'] and not any(deny_str in listing["url_key"] for deny_str in self.deny):
                yield from self.parse_listings_url(listing, f'{listing_url}/{listing["url_key"]}', meta, listing['id'])

        if listing_id:
            meta['listing_id'] = listing_id
            meta['listing_url'] = listing_url
            meta['page_number'] = 1

            yield from self.parse_pagination(meta.copy())

    def parse_pagination(self, meta):
        params = self.pagination_request_parameters(meta)
        yield Request(f'{self.products_page_url_t}{params}', method='GET', headers=self.headers,
                      callback=self.parse_category, meta=meta)

    def parse_category(self, response):
        raw_products = json.loads(response.text)['product']

        meta = response.meta.copy()
        meta['size_maps'] = self.size_maps
        meta['trail'] = self.add_trail(response)

        for raw_product in raw_products['docs']:
            params = self.product_request_parameters(raw_product)
            yield Request(f'{self.products_page_url_t}{params}', method='GET', headers=self.headers,
                          callback=self.parse_item, meta=meta)

        if raw_products['data']['next_page'] and raw_products['data']['total_count']:
            response.meta['page_number'] += 1
            yield from self.parse_pagination(response.meta)

    def pagination_request_parameters(self, meta):
        self.pagination_request_params[0][1] = str(meta["listing_id"])
        self.pagination_request_params[1][1] = str(meta["page_number"])
        return urlencode(tuple(tuple(x) for x in self.pagination_request_params))

    def product_request_parameters(self, raw_product):
        self.product_request_params[0][1] = str(raw_product["sku"])
        return urlencode(tuple(tuple(x) for x in self.product_request_params))


class ParseSpiderZA(MixinZA, ParseSpider):
    name = MixinZA.retailer + '-parse'


class CrawlSpiderZA(MixinZA, CrawlSpider):
    name = MixinZA.retailer + '-crawl'
    parse_spider = ParseSpiderZA()
