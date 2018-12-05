import json

from scrapy import Spider, Request
from w3lib.url import url_query_parameter, add_or_replace_parameter

from savagex.items import SavagexItem


class Mixin(Spider):
    retailer = 'savagex'
    allowed_domains = ['savagex.com']
    start_urls = ['http://savagex.com/']
    request_header = {}


class SavagexParseSpider(Mixin):
    name = Mixin.retailer + '_parse'
    color_url_t = 'https://www.savagex.com/api/products/{color_id}'
    BRAND = 'Savage x'
    CURRENCY = 'USD'
    GENDER = 'women'

    def parse_product(self, response):
        product = SavagexItem()
        product['skus'] = {}
        product['image_urls'] = []
        product['url'] = response.url
        product['brand'] = self.BRAND
        product['gender'] = self.GENDER
        product['trail'] = response.meta.get('trail')
        product['category'] = response.meta.get('category')
        product['name'] = self.product_name(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['description'] = self.product_description(response)
        product['requests'] = self.color_requests(response)

        yield self.request_or_item(product)

    def parse_color(self, response):
        product = response.meta.get('product')
        raw_product = json.loads(response.text)
        product['image_urls'].append(raw_product.get('image_view_list'))
        product['skus'].update(self.skus(raw_product))

        yield self.request_or_item(product)

    def skus(self, raw_product):
        color = raw_product.get('color')
        currency_and_price = self.product_currency_and_price(raw_product)
        skus = {}

        for size in self.color_sizes(raw_product):
            skus[f'{color}_{size}'] = sku = currency_and_price.copy()
            sku['color'] = color
            sku['size'] = size

        return skus

    def color_sizes(self, raw_product):
        raw_sizes = raw_product.get('related_product_id_object_list')[0]
        return [raw_size.get('size') for raw_size in raw_sizes.get('product_id_object_list')]

    def product_currency_and_price(self, raw_product):
        return {
            'currency': self.CURRENCY,
            'price': raw_product.get('retail_unit_price')
        }

    def color_requests(self, response):
        requests = []

        for color_id in self.color_ids(response):
            url = self.color_url_t.format(color_id=color_id)
            requests.append(Request(url=url, callback=self.parse_color, headers=self.request_header))

        return requests

    def request_or_item(self, product):
        requests = product['requests']
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            return request

        del product['requests']
        return product

    def color_ids(self, response):
        xpath = '//label[contains(@class, "ColorSwatch")]/@value'
        return response.xpath(xpath).extract()

    def product_description(self, response):
        xpath = '//div[contains(@class, "ProductDescription")]//text()'
        return response.xpath(xpath).extract()

    def product_retailer_sku(self, response):
        retailer_sku_r = r'"group_code":"(\w*)"'
        return response.css('script').re_first(retailer_sku_r)

    def product_name(self, response):
        xpath = '//h1[contains(@class, "ProductName")]/text()'
        return response.xpath(xpath).extract_first()


class SavagexCrawlSpider(Mixin):
    name = Mixin.retailer + '_crawl'
    product_parser = SavagexParseSpider()
    configuration_r = '__CONFIG__ = ({.*})'
    product_url_t = 'https://www.savagex.com/shop/{link}-{pid}'
    product_category_url_t = 'https://www.savagex.com/api/products?aggs=true&'\
        'includeOutOfStock=true&page=1&size=28&defaultProductCategoryIds'\
        '={category_id}&sort=newarrivals&excludeFpls=13506&warehouseId=154'

    def parse(self, response):
        self.category_request_header(response)
        yield from self.product_category_requests(response)

    def parse_category(self, response):
        yield from self.product_requests(response)
        yield self.next_page_request(response)

    def next_page_request(self, response):
        if not response:
            return

        meta = self.request_meta(response)
        url = add_or_replace_parameter(response.url, 'aggs', 'false')
        page_count = int(url_query_parameter(response.url, 'page')) + 1
        url = add_or_replace_parameter(url, 'page', page_count)

        return Request(url=url, callback=self.parse_category, headers=self.request_header, meta=meta)

    def product_requests(self, response):
        requests = []
        meta = self.request_meta(response)

        for raw_product in self.raw_products(response):
            url = self.product_url_t.format(link=raw_product['permalink'], pid=raw_product['master_product_id'])
            requests.append(Request(url=url, callback=self.product_parser.parse_product, meta=meta))

        return requests

    def raw_products(self, response):
        if not response:
            return []

        raw_products = json.loads(response.text)
        return raw_products.get('products') if isinstance(raw_products, dict) else raw_products

    def product_category_requests(self, response):
        product_categories = self.map_categories(response)
        requests = []
        trail = self.requests_trail(response)
        meta = {'trail': trail}

        for category in product_categories:
            url = self.product_category_url_t.format(category_id=product_categories[category])
            meta['category'] = category
            requests.append(Request(url=url, callback=self.parse_category, meta=meta.copy(), headers=self.request_header))

        return requests

    def requests_trail(self, response):
        return response.meta.get('trail', []) + [('', response.url)]

    def request_meta(self, response):
        return {
            'category': response.meta.get('category'),
            'trail': self.requests_trail(response),
        }

    def map_categories(self, response):
        raw_configurations = json.loads(response.css('script').re_first(self.configuration_r))
        raw_category = raw_configurations.get('productBrowser').get('sections')

        return {category: raw_category.get(category).get('defaultProductCategoryIds')
                for category in raw_category.keys()}

    def category_request_header(self, response):
        raw_header = json.loads(response.css('script').re_first(self.configuration_r)).get('api')
        self.request_header[raw_header.get('keyHeader')] = raw_header.get('key')

