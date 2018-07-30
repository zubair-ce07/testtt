import requests
import re
import json
from parsel import Selector


class Product():

    def extract_sku_features(self, selector, size, retailer_sku):
        sku = {}
        sku['color'] = selector.css('.color::text').get()
        sku['price'] = selector.css(
            '[id^=product-price] > .price::text').get()

        sku['currency'] = selector.css(
            '.inner-heading > .label::text').getall()[1]

        sku['size'] = size
        sku['previous_prices'] = selector.css(
            '[id^=old-price] > .price::text').get()

        sku['out_of_stock'] = "false"
        sku['sku_id'] = retailer_sku + "_" + size
        return sku

    def generate_skus(self, sizes, selector, retailer_sku):
        generated_skus = []
        for size in sizes:
            sku = self.extract_sku_features(selector, size, retailer_sku)
            generated_skus.append(sku)
        return generated_skus

    def extract_category(self, url):

        category = re.search(
            r'^https:\/\/[^\/]*\/[^\/]*\/[^\/]*\/([^\/]*).*', url)

        if category:
            return "sale" if "sale" in url else category.group(1)
        else:
            return ""

    def extract_image_urls(self, selector):
        images_url = []
        images_x = selector.xpath(
            '//script[@type="text/x-magento-init" and contains(text(), "mage/gallery/gallery")]/text()')

        images_script = images_x.get()
        images_script_json = json.loads(images_script)
        images_urls = images_script_json.get(
            "[data-gallery-role=gallery-placeholder]").get("mage/gallery/gallery").get("data")

        for image_urls in images_urls:
            images_url.append(image_urls.get("full"))
        return images_url

    def extract_sizes(self, selector):

        sizes_x = selector.xpath(
            '//script[contains(text(), "AEC.SUPER")]/text()')

        sizes_script = sizes_x.get()
        sizes = re.findall('\"default_label\": \"(.+?)\",', sizes_script)
        return sizes

    def parse_product(self, url):
        product = {}
        selector = Selector(requests.get(url).text)
        product['retailer_sku'] = selector.css(
            '.product.attribute.sku.custom > .value::text').get()

        product['gender'] = 'women' if 'women' in url else 'men'
        product['category'] = self.extract_category(url)
        product['brand'] = "The Upside Sport"
        product['url'] = url
        product['name'] = selector.css('.page-title > .base::text').get()
        product['description'] = selector.css(
            '.product.attribute.description > .value > .p1::text').getall()

        product['care'] = selector.css('.fabric-care > ul > li::text').getall()
        product['image_urls'] = self.extract_image_urls(selector)
        sizes = self.extract_sizes(selector)
        product['skus'] = self.generate_skus(
            sizes, selector, product['retailer_sku'])
        return product
