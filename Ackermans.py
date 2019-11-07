import json
import re

from scrapy.spiders import CrawlSpider
from itertools import product
from scrapy import Request

from ..items import AckermansItem


class AckermansParser:
    img_url_template = 'https://cdn.ackermans.co.za/product-images/prod/600_600_{}.webp'

    def parse_details(self, response):
        item = AckermansItem()
        raw_product = json.loads(response.text)['product']['docs'][0]

        sizes = response.meta['sizes']
        colors = response.meta['colors']
        category_tree = response.meta['category_tree']

        item['retailer_sku'] = self.extract_retailor_sku(raw_product)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(raw_product, category_tree)
        item['brand'] = self.extract_brand()
        item['url'] = self.extract_url(response)
        item['name'] = self.extract_name(raw_product)
        item['description'] = self.extract_description(raw_product)
        item['care'] = self.extract_care(raw_product)
        item['image_urls'] = self.extract_img_urls(raw_product)
        item['skus'] = self.extract_skus(raw_product, colors, sizes)

        yield item

    def extract_retailor_sku(self, raw_product):
        return raw_product['id']

    def extract_gender(self, response):
        gender = re.search('women|boy|girl', response.meta['tail'])
        if gender in ['women', 'girl']:
            gender = 'female'
        if gender in ['boy']:
            gender = 'male'
        return gender

    def extract_category(self, raw_product, category_tree):
        categories = raw_product['category_ids']
        return ['Home'] + [self.get_categories(category_tree['children_data'], int(category)) for category in
                           categories]

    def extract_brand(self):
        return 'ACKERMANS'

    def extract_url(self, response):
        return response.meta['tail']

    def extract_name(self, raw_product):
        return raw_product['name']

    def extract_description(self, raw_product):
        return raw_product['custom_attributes']['meta_description']

    def extract_care(self, raw_product):
        return raw_product['custom_attributes']['short_description']

    def extract_img_urls(self, raw_product):
        return self.img_url_template.format(raw_product['custom_attributes']['image_name'])

    def extract_common_sku(self, raw_product):
        sku = {'currency': 'ZAR'}
        sku['previous_price'] = []
        sku['price'] = raw_product['price']
        sku['out_of_stock'] = False
        return sku

    def extract_skus(self, raw_product, colors_val, sizes_val):
        common_sku = self.extract_common_sku(raw_product)
        colors = raw_product['custom_attributes']['color_ids']
        sizes = raw_product['custom_attributes']['size_ids']
        skus = []
        for color, size in product(colors, sizes):
            sku = common_sku.copy()
            sku['size'] = self.get_requiered_size_color(sizes_val, size)
            sku['color'] = self.get_requiered_size_color(colors_val, color)
            sku['sku_id'] = f'{sku["color"]}_{sku["size"]}'
            skus.append(sku)
        return skus

    def get_requiered_size_color(self, collection, code):
        for object in collection:
            if object['value'] == str(code):
                return object['label']

    def get_categories(self, category_tree, category_id):
        for category in category_tree:
            if category['id'] == category_id:
                return category['name']
        for category in category_tree:
            category_name = self.get_categories(category['children_data'], category_id)
            if category_name:
                return category_name


class AckermansSpider(CrawlSpider):
    name = 'ackermans'
    allowed_domains = ['www.ackermans.co.za', 'magento.ackermans.co.za']
    
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer x3leg25sl1vvruoa6vr861vgus503cfq'}
    ackerman_parser = AckermansParser()
    category_template = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/searchV2?' \
                        'search_criteria%5Bcurrent_page%5D={}&' \
                        'search_criteria%5Bfilter_groups%5D%5B2%5D%5Bfilters%5D%5B0%5D%5Bfield%5D=category_ids' \
                        '&search_criteria%5Bfilter_groups%5D%5B2%5D%5Bfilters%5D%5B0%5D%5Bvalue%5D={}&' \
                        'search_criteria%5Bpage_size%5D=20&search_criteria%5Bsort_orders%5D%5B0%5D%5Bfield%5D=price'
    product_url_tempelate = 'https://www.ackermans.co.za{}/{}'
    product_detail_tempelate = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/searchV2?' \
                               'search_criteria%5Bfilter_groups%5D%5B0%5D%5Bfilters%5D%5B0%5D%5Bfield%5D=sku&' \
                               'search_criteria%5Bfilter_groups%5D%5B0%5D%5Bfilters%5D%5B0%5D%5Bvalue%5D={}&' \
                               'search_criteria%5Bpage_size%5D=1'
    color_size_req_tempelate = 'https://magento.ackermans.co.za/rest/default/V1/products/attributes?' \
                               'search_criteria%5Bfilter_groups%5D%5B0%5D%5Bfilters%5D%5B0%5D%5Bfield%5D=attribute_code&' \
                               'search_criteria%5Bfilter_groups%5D%5B0%5D%5Bfilters%5D%5B0%5D%5Bvalue%5D={}'
    categories_url = 'https://magento.ackermans.co.za/rest/default/V1/pepkor/categoryapi/categories'

    def start_requests(self):
        urls = [
            'https://magento.ackermans.co.za/rest/default/V1/pepkor/categoryapi/categories',
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        category_tree = json.loads(response.text)
        yield response.follow(self.color_size_req_tempelate.format('size'), callback=self.parse_sizes,
                              headers=self.headers, meta={'category_tree': category_tree})

    def parse_sizes(self, response):
        sizes = json.loads(response.text)['items'][0]['options']
        category_tree = response.meta['category_tree']
        yield response.follow(self.color_size_req_tempelate.format('color'), callback=self.parse_colors,
                              headers=self.headers, meta={'sizes': sizes, 'category_tree': category_tree})

    def parse_colors(self, response):
        sizes = response.meta['sizes']
        category_tree = response.meta['category_tree']
        colors = json.loads(response.text)['items'][0]['options']

        categories = self.make_urls(category_tree)
        for category in categories:
            url = self.category_template.format('1', category['id'])
            yield response.follow(url, callback=self.parse_category, headers=self.headers,
                                  meta={'tail': category['url_key'], 'id': category['id'],
                                        'category_tree': category_tree, 'sizes': sizes, 'colors': colors})

    def parse_category(self, response):
        raw_products = json.loads(response.text)
        products = raw_products['product']['docs']
        tail = response.meta['tail']
        id = response.meta['id']
        category_tree = response.meta['category_tree']
        sizes = response.meta['sizes']
        colors = response.meta['colors']

        if raw_products['product']['data']['next_page'] & raw_products['product']['data']['total_count'] > 0:
            next_page_num = raw_products['product']['data']['current_page'] + 1
            url = self.category_template.format(next_page_num, id)
            yield response.follow(url, callback=self.parse_category, headers=self.headers,
                                  meta={'tail': tail, 'id': id, 'category_tree': category_tree,
                                        'sizes': sizes, 'colors': colors})

        for product in products:
            product_url = self.product_url_tempelate.format(tail, product['url_key'])
            url = self.product_detail_tempelate.format(product['sku'])
            yield response.follow(url, callback=self.ackerman_parser.parse_details, headers=self.headers,
                                  meta={'tail': product_url, 'category_tree': category_tree,
                                        'sizes': sizes, 'colors': colors})

    def make_urls(self, url_tree):
        node_key = url_tree['url_key']
        node_id = url_tree['id']
        urls = [{'id': node_id, 'url_key': f'/{node_key}'}] if url_tree['level'] > 2 else []

        if node_key == 'default-category':
            node_key = 'product'
        if node_key in ['deals', 'cellular']:
            return []

        for children in url_tree['children_data']:
            if children['is_active']:
                childs = self.make_urls(children)
                urls += [{'id': child['id'], 'url_key': f'/{node_key}{child["url_key"]}'} for child in childs]
        return urls


class AckermansItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()

