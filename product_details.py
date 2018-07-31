import requests
import re
import json
from parsel import Selector


class ProductParser:

    @staticmethod
    def extract_sku_features(selector):
        return {
            'color':            selector.css('.color::text').get(),
            'price':            selector.css('[id^=product-price] > .price::text').get(),
            'currency':         selector.css('.inner-heading > .label::text').getall()[1],
            'previous_price':   selector.css('[id^=old-price] > .price::text').get()
        }

    @staticmethod
    def extract_sizes(selector):
        sizes_x = selector.xpath('//script[contains(text(), "AEC.SUPER")]/text()')
        sizes_script = sizes_x.get()
        sizes = re.findall('\"default_label\": \"(.+?)\",', sizes_script)
        return sizes

    @staticmethod
    def generate_skus(selector):
        generated_skus = {}
        sizes = ProductParser.extract_sizes(selector)
        common_sku = ProductParser.extract_sku_features(selector)
        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = size
            generated_skus[size] = sku
        return generated_skus

    @staticmethod
    def extract_image_urls(selector):
        images_x = selector.xpath('//script[@type="text/x-magento-init" and contains(text(), "mage/gallery/gallery")]/text()')
        images_script = images_x.get()
        images_script_json = json.loads(images_script)
        images_urls = images_script_json["[data-gallery-role=gallery-placeholder]"]["mage/gallery/gallery"]["data"]
        return [image_urls["full"] for image_urls in images_urls]

    @staticmethod
    def extract_care(selector):
        return selector.css('.fabric-care > ul > li::text').getall()

    @staticmethod
    def extract_description(selector):
        return selector.css('.product.attribute.description > .value > .p1::text').getall()

    @staticmethod
    def extract_prod_name(selector):
        return selector.css('.page-title > .base::text').get()

    @staticmethod
    def extract_category(url):
        category = url.split("/")
        return category[-2:-1]

    @staticmethod
    def extract_gender(url):
        return 'women' if 'women' in url else 'men'

    @staticmethod
    def extract_retailer_sku(selector):
        return selector.css('.product.attribute.sku.custom > .value::text').get()

    @staticmethod
    def parse_product(url):
        selector = Selector(requests.get(url).text)
        return {

            'retailer_sku': ProductParser.extract_retailer_sku(selector),
            'gender':       ProductParser.extract_gender(url),
            'category':     ProductParser.extract_category(url),
            'brand':        "The Upside Sport",
            'url':          url,
            'name':         ProductParser.extract_prod_name(selector),
            'description':  ProductParser.extract_description(selector),
            'care':         ProductParser.extract_care(selector),
            'image_urls':   ProductParser.extract_image_urls(selector),
            'skus':         ProductParser.generate_skus(selector)
        }
