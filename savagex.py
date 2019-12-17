import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request

from .base import BaseCrawlSpider, BaseParseSpider, Gender


class Mixin:
    gender = Gender.WOMEN.value
    retailer = 'savagex'
    ajex_req_url = 'https://www.savagex.co.uk/api/products'


class MixinUK(Mixin):
    market = 'UK'
    currency = 'GBP'
    retailer = Mixin.retailer + '-uk'
    allowed_domains = ['savagex.co.uk']
    start_urls = ['https://www.savagex.co.uk/']


class SavagexSpider(BaseParseSpider):

    def parse(self, response):
        raw_product = json.loads(response.text)

        garment = self.new_unique_garment(self.product_id(raw_product))
        if not garment:
            return

        self.boilerplate_minimal(garment, response)
        garment['trail'] = self.add_trail(response)
        garment['name'] = self.product_name(raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['gender'] = self.product_gender()
        garment['category'] = self.product_category(response)
        garment['brand'] = self.product_brand(response)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.product_skus(raw_product)
        garment['meta'] = {'image_requests': self.image_requests(response, raw_product)}
        return self.garment_or_next_images(garment)

    def garment_or_next_images(self, garment):
        image_reqs = garment['meta']['image_requests']

        if image_reqs:
            req = garment['meta']['image_requests'].pop()
            req.meta['garment'] = garment
            yield req
        else:
            garment.pop('meta')
            yield garment

    def images_request(self, response):
        garment = response.meta['garment']
        raw_data = json.loads(response.text)
        garment['image_urls'] += self.image_urls(raw_data)
        return self.garment_or_next_images(garment)

    def product_id(self, raw_data):
        return raw_data['master_product_id']

    def product_name(self, raw_product):
        return raw_product['label']

    def raw_description(self, response, **kwargs):
        return [''.join([response.get('long_description') or '', response.get('medium_description') or ''])]

    def product_gender(self):
        return self.gender

    def product_category(self, raw_product):
        return []

    def image_urls(self, raw_product):
        return raw_product['image_view_list']

    def product_skus(self, raw_product):
        common_sku = self.common_sku(raw_product)
        raw_skus = raw_product['related_product_id_object_list']

        skus = {}
        for raw_sku in raw_skus:
            sku = common_sku.copy()
            color = raw_sku['color']
            sku['colour'] = color
            raw_sizes = raw_sku['product_id_object_list']
            for raw_size in raw_sizes:
                size_sku = sku.copy()
                size = raw_size['size']
                size_sku['size'] = size
                skus[f'{color}_{size}'] = size_sku
        return skus

    def common_sku(self, raw_product):
        return {
            'price': raw_product['retail_unit_price'],
            'previous_prices': [raw_product['default_unit_price']] or [],
            'currency': self.currency
        }

    def image_requests(self, response,raw_product):
        products = raw_product['related_product_id_object_list']
        headers = response.meta['headers']
        image_requests = []
        for product in products:
            url = f'{self.ajex_req_url}/{product["related_product_id"]}'
            if url == response.url:
                continue
            image_requests.append(Request(url=url, headers=headers, callback=self.images_request))

        return image_requests

class SavagexCrawler(BaseCrawlSpider):
    product_listing = r'/products/'
    custom_settings = {
        'DOWNLOAD_DELAY': '1'
    }

    rules = (
        Rule(LinkExtractor(allow=product_listing), callback='parse_listing'),
    )

    def parse(self, response):
        raw_info = response.css('#__NEXT_DATA__::text').get()
        raw_info = json.loads(raw_info)

        api_key = raw_info['runtimeConfig']['bentoApi']['key']
        headers = {
            'origin': 'https://www.savagex.co.uk',
            'x-api-key': api_key,
        }
        meta = {'headers': headers,
                'trail': self.add_trail(response)}

        yield from[Request(url=self.ajex_req_url+'/categorized', headers=headers, body=body, method='POST',
                           callback=self.parse_products, meta=meta) for body in self.requests_body(raw_info)]

    def parse_products(self, response):
        headers = response.meta['headers']
        raw_products = json.loads(response.text)
        products = raw_products['products']

        new_header = headers.copy()
        new_header.pop('origin')
        new_header['x-tfg-storedomain'] = 'www.savagex.co.uk'
        meta = {
            'trail': self.add_trail(response),
            'headers': new_header
        }

        yield from [Request(url=f'{self.ajex_req_url}/{product["master_product_id"]}', headers=new_header,
                          callback=self.parse_item, meta=meta) for product in products]

        body = json.loads(response.request.body.decode('utf-8'))
        body['page'] = body['page'] + 1

        if raw_products['pages'] <= body['page']:
            return

        yield Request(url=self.ajex_req_url, headers=headers, body=json.dumps(body), method='POST',
                      callback=self.parse_products, meta={'headers': headers, 'trail': self.add_trail(response)})

    def requests_body(self, raw_info):
        raw_categories = raw_info['runtimeConfig']['productBrowser']['sections'] or {}
        for category_info in raw_categories.values():
            sub_categories = category_info['subsections']
            return [self.make_req_body(sub_cat['categoryTagIds']) for sub_cat in sub_categories.values()]

    def make_req_body(self, cat_id, page_no=1):
        return f'{{"includeOutOfStock": "true", "page": {page_no}, "size": 28, "categoryTagIds": {cat_id}}}'


class SavagexUKSpider(MixinUK, SavagexSpider):
    name = MixinUK.retailer + '-parse'


class SavagexUKCrawler(MixinUK, SavagexCrawler):
    name = MixinUK.retailer + '-crawl'
    parse_spider = SavagexUKSpider()
