import json
import itertools
from urllib.parse import urljoin

from scrapy import Spider, Request

from lanebryant.items import LanebryantItem


class ProductParser(Spider):
    name = "lanebryant-parser"
    brand = "LB"
    gender = "women"
    item_regex = "\{.*\:\{.*\:.*\}\}"
    visited = set()

    def parse(self, response):
        retailer_sku = self.extract_retailer_sku(response)
        if retailer_sku in self.visited:
            return

        item = LanebryantItem()
        item['retailer_sku'] = retailer_sku
        item['url'] = response.url
        item['brand'] = self.brand
        item['gender'] = self.gender
        item['image_urls'] = []
        item['name'] = self.extract_name(response)
        item['price'] = self.extract_price(response)
        item['trail'] = self.extract_trails(response)
        item['currency'] = self.extract_currency(response)
        item['care'] = self.extract_product_care(response)
        item['category'] = self.extract_category(response)
        item['skus'] = self.extract_skus(response)
        item['description'] = self.extract_product_description(response)
        item['requests'] = self.image_requests(response, retailer_sku)
        self.visited.add(retailer_sku)
        return self.parse_requests(item)

    def parse_requests(self, item):
        if not item['requests']:
            del item['requests']
            return item

        request = item['requests'].pop()
        request.meta['item'] = item
        yield request

    def image_requests(self, response, retailer_sku):
        raw_product = self.extract_raw_product(response)
        raw_colors = self.get_item_map(raw_product, 'all_available_colors',
                                       'name')

        raw_server_url = raw_product['pdpDetail']['product'][0]['scene7_params']
        server_url = f"http:{raw_server_url['server_url']}"
        request_url = "{}lanebryantProdATG/{}_ms?req=set,json"

        return [Request(url=request_url.format(server_url, f"{retailer_sku}_{color}"),
                        callback=self.parse_image_urls,
                        meta={'base_url': server_url}) for color in raw_colors]

    def parse_image_urls(self, response):
        item = response.meta['item']
        base_url = response.meta['base_url']
        item['image_urls'] += self.extract_image_urls(response, base_url)
        return self.parse_requests(item)

    def extract_image_urls(self, response, base_url):
        image_regex = self.item_regex
        raw_image_urls = json.loads(response.css("p::text").re(image_regex)[0])

        return [urljoin(base_url, url['i']['n'])
                for url in raw_image_urls['set']['item']]

    def extract_trails(self, response):
        return response.meta.get('trail')

    def extract_retailer_sku(self, response):
        return response.css("::attr(data-bv-product-id)").extract_first()

    def extract_name(self, response):
        return response.css(".mar-product-title::text").extract_first()

    def extract_product_care(self, response):
        return response.css("#tab1 ul:nth-child(3) ::text").extract()

    def extract_product_description(self, response):
        description_css = "#tab1 p::text, #tab1 ul:nth-child(2) ::text"
        return response.css(description_css).extract()

    def extract_raw_product(self, response):
        return json.loads(response.css("#pdpInitialData::text").extract_first())

    def extract_price_specification(self, response):
        price_specification_css = "[type='application/ld+json']::text"
        return json.loads(response.css(price_specification_css).extract_first())

    def extract_price(self, response):
        raw_price = self.extract_price_specification(response)
        return raw_price['offers']['priceSpecification']['price']

    def extract_currency(self, response):
        raw_currency = self.extract_price_specification(response)
        return raw_currency['offers']['priceSpecification']['priceCurrency']

    def extract_category(self, response):
        category_css = "script:contains('breadcrumbs')::text"
        category_regex = self.item_regex

        raw_categories = json.loads(response.css(category_css).re(category_regex)[0])
        return raw_categories['page']['breadcrumbs'].split('|')

    def extract_raw_skus(self, response):
        raw_skus = self.extract_raw_product(response)
        return raw_skus['pdpDetail']['product'][0]['skus']

    def get_item_map(self, raw_product, item_key, item_name):
        raw_info = raw_product['pdpDetail']['product'][0][item_key][0]['values']
        return {info['id']: info[item_name] for info in raw_info}

    def extract_skus(self, response):
        raw_product = self.extract_raw_product(response)
        color_map = self.get_item_map(raw_product, 'all_available_colors', 'name')
        size_map = self.get_item_map(raw_product, 'all_available_sizes', 'value')
        sku_info = {
            'currency': self.extract_currency(response),
            'price': self.extract_price(response)
        }

        skus = {}
        for raw_sku in self.extract_raw_skus(response):
            sku = sku_info.copy()
            sku['color'] = color_map[raw_sku['color']]
            sku['size'] = size_map[raw_sku['size']]
            skus[raw_sku['sku_id']] = sku
        return skus
