import json
import re

from scrapy import Spider, Request

from maurices.items import MauricesProduct


class MauricesParseProduct(Spider):
    name = 'maurices_parse_product'
    color_url_t = 'https://mauricesprodatg.scene7.com/is/image/mauricesProdATG/' \
        '{pid}_{color_id}_ms?req=set,json&id={color_id}'
    BRAND = 'maurices'
    CURRENCY = 'USD'

    def parse_product(self, response):
        product = MauricesProduct()
        product['image_urls'] = []
        product['brand'] = self.BRAND
        product['url'] = response.url
        product['name'] = self.product_name(response)
        product['skus'] = self.product_skus(response)
        product['category'] = self.product_category(response)
        product['description'] = self.product_description(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['requests'] = self.color_requests(response)

        yield self.request_or_item(product)

    def parse_color(self, response):
        product = response.meta.get('product')
        product['image_urls'].extend(self.image_urls(response))

        yield self.request_or_item(product)

    def request_or_item(self, product):
        requests = product['requests']
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            return request

        del product['requests']
        return product

    def image_urls(self, response):
        return list(set(re.findall(r'mauricesProdATG/[^"]*', response.text)))

    def available_sku_keys(self, raw_product):
        colors = self.attribute_map(raw_product['all_available_colors'])
        sizes = self.attribute_map(raw_product['all_available_sizes'])
        available_sku_keys = []

        for raw_sku in raw_product['skus']:
            sku_key = f"{colors.get(raw_sku['color'])}_{sizes.get(raw_sku['size'])}"
            available_sku_keys.append(sku_key)

        return available_sku_keys

    def color_requests(self, response):
        raw_product = self.raw_product(response)
        product_id = self.product_retailer_sku(response)
        colors = self.attribute_map(raw_product['all_available_colors'])
        requests = []

        for color_id in colors:
            url = self.color_url_t.format(pid=product_id, color_id=color_id)
            requests.append(Request(url, callback=self.parse_color))

        return requests

    def product_skus(self, response):
        raw_product = self.raw_product(response)
        available_sku_keys = self.available_sku_keys(raw_product)
        colors = self.attribute_map(raw_product['all_available_colors'])
        sizes = self.attribute_map(raw_product['all_available_sizes'])
        product_currency_and_price = self.product_currency_and_price(response)
        skus = {}

        for color_id in colors:
            for size_id in sizes:
                sku_key = str(colors[color_id] + '_' + sizes[size_id])
                skus[sku_key] = {
                    'color': colors[color_id],
                    'size': sizes[size_id],
                }
                skus[sku_key].update(product_currency_and_price)

                if sku_key not in available_sku_keys:
                    skus[sku_key]['out_of_stock'] = True

        return skus

    def product_currency_and_price(self, response):
        raw_product = self.raw_product(response)
        prices = raw_product['all_available_colors'][0]['values'][0]['prices']
        curr_price = prices['sale_price']
        previous_price = prices['list_price']
        currency_and_price = {
            'currency': self.CURRENCY,
            'price': curr_price,
        }

        if curr_price != previous_price:
            currency_and_price['previous_price'] = previous_price

        return currency_and_price

    def raw_product(self, response):
        css = '#pdpInitialData::text'
        product_data = response.css(css).extract_first()
        return json.loads(product_data)['pdpDetail']['product'][0]

    def product_category(self, response):
        raw_product = self.raw_product(response)
        return raw_product['ensightenData'][0]['categoryPath']

    def product_name(self, response):
        name_css = '.mar-product-title::text'
        return response.css(name_css).extract_first()

    def product_description(self, response):
        description_css = '.mar-product-description-content li::text'
        return response.css(description_css).extract()

    def product_retailer_sku(self, response):
        return response.url.split('/')[-1]

    def attribute_map(self, raw_attributes):
        if not raw_attributes:
            return {}

        return {str(attribute['id']): str(attribute['value']) for attribute in raw_attributes[0]['values']}

