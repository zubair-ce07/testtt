import json
import re
from collections import defaultdict

import parsel


class ProductParser:

    def __init__(self):
        self.seen_products = set()

    def parse(self, response):
        response_s = parsel.Selector(text=response.text)
        product_id = self.product_id(response_s)

        if not product_id:
            return
        if product_id in self.seen_products:
            return
        self.seen_products.add(product_id)

        product = {
            'retailer_sku': product_id,
            'brand': 'LIUJO',
            'url': response.url,
            'name': self.product_name(response_s),
            'description': self.product_description(response_s),
            'care': self.product_care(response_s),
            'image_urls': self.image_urls(response_s),
            'skus': self.product_skus(response_s)
        }

        return product

    def product_id(self, selector):
        return selector.css(".product-ids::attr('data-sku')").get()

    def product_name(self, selector):
        return selector.css(".product-name > h1::text").get()

    def product_description(self, selector):
        css = ".short-description-value ::text"
        return selector.css(css).getall()

    def product_care(self, selector):
        return selector.css(".details-value p::text").getall()

    def image_urls(self, selector):
        return selector.css(".product-media-gallery-inner img::attr('src')").getall()

    def product_skus(self, selector):
        product_id = self.product_id(selector)
        sku_css = '.product-options script'
        script_regex = r'\s*var\s\w+\s=\snew\sProduct\.\w+\((.+)\);'
        raw_skus = json.loads(selector.css(sku_css).re_first(script_regex))
        currency_re = re.compile("\w{3}$")

        skus_map = {}
        for attribute in raw_skus['attributes'].values():
            for option in attribute['options']:
                for sku_id in option['products']:
                    skus_map[sku_id] = skus_map.setdefault(sku_id, {})
                    skus_map[sku_id][attribute['code']] = option

        skus = {}
        for sku_id, raw_attribute in skus_map.items():
            sku = {}
            if raw_attribute.get('color'):
                sku["colour"] = raw_attribute.get('color').get('label')
            sku.update({
                "price": raw_skus.get('basePrice'),
                "currency": currency_re.search(raw_skus.get('template')).group(0),
                "size": raw_attribute.get('liujo_size').get('label') if raw_attribute.get('liujo_size') else 'unisize',
                "previous_prices": raw_skus.get('oldPrice'),
                "sku_id": f"{product_id}_{sku_id}"
            })

            color_ids = set(raw_attribute.get('color').get('products'))
            size_ids = set(raw_attribute.get('liujo_size').get('products'))

            if not color_ids & size_ids:
                sku["out_of_stock"] = True
            skus[sku_id] = sku

        return list(skus.values())
