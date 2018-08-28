import json
import itertools

from scrapy import Spider

from lanebryant.items import LanebryantItem


class ProductParser(Spider):
    name = 'lanebryant-parser'
    brand = 'LB'
    gender = 'female'
    visited = set()

    def parse(self, response):
        retailer_sku = self.extract_retailer_sku(response)
        if retailer_sku in self.visited:
            return

        price = self.extract_price(response)
        currency = self.extract_currency(response)

        item = LanebryantItem()
        item['retailer_sku'] = retailer_sku
        item['url'] = response.url
        item['price'] = price
        item['currency'] = currency
        item['brand'] = self.brand
        item['gender'] = self.gender
        item['name'] = self.extract_name(response)
        item['description'] = self.extract_product_description(response)
        item['care'] = self.extract_product_care(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['trail'] = self.extract_trails(response)
        item['category'] = self.extract_category(response)
        item['skus'] = self.extract_skus(response, price, currency)
        self.visited.add(retailer_sku)
        return item

    def extract_trails(self, response):
        return response.meta.get('trail')

    def extract_retailer_sku(self, response):
        return response.css('::attr(data-bv-product-id)').extract_first()

    def extract_category(self, response):
        category_css = "script:contains('breadcrumbs')::text"
        category_regex = 'window.lanebryantMarketingDL = (.*?);\s*$'
        raw_breadcrumbs = json.loads(response.css(category_css).re(category_regex)[0])
        return raw_breadcrumbs['page']['breadcrumbs'].split('|')

    def extract_name(self, response):
        return response.css('.mar-product-title::text').extract_first()

    def extract_product_care(self, response):
        return response.css('#tab1 ul:nth-child(3) ::text').extract()

    def extract_product_description(self, response):
        description = response.css('#tab1 p::text').extract()
        description += response.css('#tab1 ul:nth-child(2) ::text').extract()
        return description

    def extract_raw_product(self, response):
        return json.loads(response.css('#pdpInitialData::text').extract_first())

    def extract_price_specification(self, response):
        price_specification_css = "[type='application/ld+json']::text"
        return json.loads(response.css(price_specification_css).extract_first())

    def extract_image_urls(self, response):
        return self.extract_price_specification(response)['image']

    def extract_price(self, response):
        raw_price = self.extract_price_specification(response)
        return raw_price['offers']['priceSpecification']['price']

    def extract_currency(self, response):
        raw_currency = self.extract_price_specification(response)
        return raw_currency['offers']['priceSpecification']['priceCurrency']

    def extract_raw_skus(self, response):
        raw_skus = self.extract_raw_product(response)
        return raw_skus['pdpDetail']['product'][0]['skus']

    def extract_color(self, raw_product, color_id):
        raw_colors = raw_product['pdpDetail']['product'][0]
        for color in raw_colors['all_available_colors'][0]['values']:
            if color_id == color['id']:
                return color['name']

    def extract_size(self, raw_product, size_id):
        raw_sizes = raw_product['pdpDetail']['product'][0]
        for size in raw_sizes['all_available_sizes'][0]['values']:
            if size_id == size['id']:
                return size['value']

    def extract_unavailable_sizes(self, raw_product):
        available_sizes = raw_product['all_available_size_groups'][0]['values'][0]['values']
        in_stock = raw_product['all_available_sizes'][0]['values']

        in_stock = {sku['value'] for sku in in_stock}
        return [size for size in available_sizes if size['value'] not in in_stock]

    def extract_out_of_stock_skus(self, raw_product, currency, price):
        colors = raw_product['all_available_colors'][0]['values']
        if 'all_available_size_groups' not in raw_product:
            return

        skus = {}
        unavailable_sizes = self.extract_unavailable_sizes(raw_product)
        for color, size in itertools.product(colors, unavailable_sizes):
            skus[f"{color['id']}_{size['id']}"] = {
                'color': color['name'],
                'currency': currency,
                'out_of_stock': True,
                'prices': {
                    'list_price': f"${price}",
                    'sale_price': f"${price}"
                },
                'size': size['value']
            }
        return skus

    def extract_skus(self, response, price, currency):
        raw_skus = self.extract_raw_skus(response)
        raw_product = self.extract_raw_product(response)

        skus = {}
        for sku in raw_skus:
            id = f"{sku['color']}_{sku['size']}"
            sku['currency'] = currency
            sku['color'] = self.extract_color(raw_product, sku['color'])
            sku['size'] = self.extract_size(raw_product, sku['size'])
            del sku['sku_id']
            skus[id] = sku.copy()

        out_of_stock_skus = self.extract_out_of_stock_skus(raw_product['pdpDetail']['product'][0],
                                                           currency, price)
        if out_of_stock_skus:
            skus.update(out_of_stock_skus)
        return skus
