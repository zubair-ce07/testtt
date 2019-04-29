import re
import json
from urllib.parse import unquote

from scrapy.spiders import Request
from w3lib.url import add_or_replace_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'ackermans'
    default_brand = 'Ackermans'
    allowed_domains = ['ackermans.co.za']


class MixinZA(Mixin):
    retailer = Mixin.retailer + '-za'
    market = 'ZA'
    currency = 'ZAR'
    start_urls = ['https://www.ackermans.co.za/']

    unwanted_items = ['toys', 'airtime-and-data', 'amajoya-sweets-promotion']
    homeware_categories = ['homeware', 'furniture', 'decor', 'home', 'bed', 'bath']

    headers = {
        'Origin': 'https://www.ackermans.co.za',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Bearer x3leg25sl1vvruoa6vr861vgus503cfq',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }

    product_url_t = 'https://www.ackermans.co.za/product/{}/{}'
    image_url_t = 'https://cdn.ackermans.co.za/product-images/prod/1100_1100_{}.jpg'
    categories_url = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/categoryapi/categories'

    category_url_t = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/searchV2?search_criteria%5B' \
                     'current_page%5D=1&search_criteria%5Bfilter_groups%5D%5B2%5D%5Bfilters%5D%5B0%5D%5B' \
                     'field%5D=category_ids&search_criteria%5Bfilter_groups%5D%5B2%5D%5Bfilters%5D%5B0%5D' \
                     '%5Bvalue%5D={}&search_criteria%5Bpage_size%5D=20'

    api_url_t = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/searchV2?' \
                'search_criteria%5Bfilter_groups%5D%5B0%5D%5Bfilters%5D%5B0%5D%5Bfield%5D=sku&' \
                'search_criteria%5Bfilter_groups%5D%5B0%5D%5Bfilters%5D%5B0%5D%5Bvalue%5D={}&' \
                'search_criteria%5Bpage_size%5D=1'

    size_and_colour_url = 'https://magento.ackermans.co.za/rest/default/V1/products/attributes?' \
                          'search_criteria%5Bfilter_groups%5D%5B0%5D%5Bfilters%5D%5B0%5D%5Bfield%5D' \
                          '=is_filterable_in_grid&search_criteria%5Bfilter_groups%5D%5B0%5D%5B' \
                          'filters%5D%5B0%5D%5Bvalue%5D=1'


class AckermansParseSpider(BaseParseSpider):
    sizes_map = {}
    colours_map = {}

    def parse(self, response):
        raw_product = self.raw_product(response)
        garment = self.new_unique_garment(self.product_id(raw_product))

        if not garment:
            return

        self.boilerplate_minimal(garment, response, self.product_url(raw_product))

        garment['url_original'] = response.url
        garment['care'] = self.product_care(raw_product)
        garment['name'] = self.product_name(raw_product)
        garment["gender"] = self.product_gender(garment)
        garment['brand'] = self.product_brand(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['image_urls'] = self.product_image_urls(raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['skus'] = self.skus(raw_product)

        if self.is_homeware(response):
            garment['industry'] = 'homeware'
            garment["gender"] = None

        return garment

    def product_id(self, raw_product):
        return raw_product['sku']

    def product_name(self, raw_product):
        return raw_product['name']

    def raw_product(self, response):
        return json.loads(response.text)['product']['docs'][0]

    def brand_soup(self, raw_product):
        return clean(raw_product['custom_attributes'].get('meta_title', ''))

    def product_description(self, raw_product):
        return [raw_product['custom_attributes'].get('meta_description', [])]

    def product_url(self, raw_product):
        raw_product["url_key"] = raw_product["url_key"].replace('\n', '')

        if not raw_product["sku"] in raw_product["url_key"]:
            return self.product_url_t.format(raw_product["url_key"], raw_product["sku"])

        url_key = '-'.join([i for i in raw_product["url_key"].split('-') if i != raw_product["sku"]])
        return self.product_url_t.format(url_key, raw_product["sku"])

    def raw_description(self, raw_product):
        return re.split('\.\s', raw_product['custom_attributes'].get('meta_description', ''))

    def product_category(self, raw_product):
        return clean(raw_product['custom_attributes'].get('meta_title', [])).split('|')[1:]

    def product_gender(self, garment):
        soup = soupify([garment['name']] + garment['category'])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, raw_product):
        skus = {}
        money_strs = [raw_product['prices']['minimal_price'], raw_product['prices']['price'], self.currency]
        common_sku = self.product_pricing_common(None, money_strs=money_strs)

        if not (raw_product['color_ids'] and raw_product['size_ids']):
            common_sku['size'] = self.one_size
            skus[self.one_size] = common_sku
            return skus

        for colour_code in raw_product['color_ids']:
            for size_code in raw_product['size_ids']:
                sku = common_sku.copy()
                sku['colour'] = self.colours_map[str(colour_code)]
                sku['size'] = self.sizes_map[str(size_code)]

                if not raw_product['extension_attributes']['stock_item'].get('is_in_stock'):
                    sku['out_of_stock'] = True

                skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus

    def product_image_urls(self, raw_product):
        image_url = raw_product['custom_attributes'].get('image_name')
        return [self.image_url_t.format(image_url)] if image_url else []

    def is_homeware(self, response):
        return any(homeware in response.meta['category_name'] for homeware in self.homeware_categories)


class AckermansCrawlSpider(BaseCrawlSpider):
    def start_requests(self):
        yield Request(url=self.categories_url, headers=self.headers, callback=self.parse_categories)

    def parse_categories(self, response):
        response.meta['trail'] = self.add_trail(response)
        yield Request(url=self.size_and_colour_url, headers=self.headers, callback=self.parse_sizes_and_colours)

        for url in self.category_ids(response):
            response.meta['category_name'] = url['category_name'].lower()

            if any(unwanted in response.meta['category_name'] for unwanted in self.unwanted_items):
                continue

            yield Request(url=self.category_url_t.format(url['category_id']), meta=response.meta.copy(),
                          headers=self.headers, callback=self.parse_pagination)

    def parse_pagination(self, response):
        page_size = 20
        products_counts = json.loads(response.text)['product']['data']['total_count']
        response.meta['trail'] = self.add_trail(response)
        pages = int(products_counts)//page_size+2

        for page in range(1, pages):
            next_url = add_or_replace_parameter(unquote(response.url), 'search_criteria[current_page]', page)
            yield Request(url=next_url, headers=self.headers, meta=response.meta.copy(),
                          callback=self.parse_listings)

    def parse_listings(self, response):
        product_ids = [i['sku'] for i in json.loads(response.text)['product']['docs']]
        response.meta['trail'] = self.add_trail(response)

        for product_id in product_ids:
            yield Request(url=self.api_url_t.format(product_id), meta=response.meta.copy(),
                          headers=self.headers, callback=self.parse_item)

    def category_ids(self, response):
        requests_ids = []
        raw_categories = json.loads(response.text)
        self.get_category_ids(raw_categories['children_data'], requests_ids)
        return requests_ids

    def get_category_ids(self, children_categories, requests_ids, category_trail=None):

        for child_category in children_categories:

            if child_category['level'] == 2:
                category_trail = child_category['url_key']

            if child_category['level'] >= 3:
                categories = category_trail + ' ' + child_category['url_key']
                requests_ids.append({'category_name': categories, 'category_id': child_category['id']})

            self.get_category_ids(child_category['children_data'], requests_ids, category_trail)

    def parse_sizes_and_colours(self, response):

        if response:
            raw_colours_sizes_maps = json.loads(response.text)['items']

            for map in raw_colours_sizes_maps:

                if map['attribute_code'] == 'color':
                    self.parse_spider.colours_map = {i['value']: i['label'] for i in map['options']}

                if map['attribute_code'] == 'size':
                    self.parse_spider.sizes_map = {i['value']: i['label'] for i in map['options']}

        else:
            yield Request(url=self.size_and_colour_url, headers=self.headers, callback=self.parse_sizes_and_colours)


class AckermansZAParseSpider(MixinZA, AckermansParseSpider):
    name = MixinZA.retailer + '-parse'


class AckermansZACrawlSpider(MixinZA, AckermansCrawlSpider):
    name = MixinZA.retailer + '-crawl'
    parse_spider = AckermansZAParseSpider()
