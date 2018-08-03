import re
import json
from scrapy import Spider
from piazza.items import SkuItem, ProductItem


class ProductParser(Spider):
    name = "piazza-parse"

    def parse(self, response):
        product = ProductItem(brand="Piazzaitalia", market="IT", retailer='piazzaitalia-it', currency="EUR")
        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['trail'] = self.extract_trail(response)
        product['gender'] = self.extract_gender(response)
        product['category'] = self.extract_category(response)
        product['url'] = response.url
        product['name'] = self.extract_prod_name(response)
        product['description'] = self.extract_description(response)
        product['care'] = self.extract_care(response)
        product['image_urls'] = self.extract_image_urls(response)
        product['skus'] = self.generate_skus(response)
        product['price'] = self.extract_price(response)
        product['spider_name'] = self.name
        return product

    def extract_price(self, response):
        price = response.css('[id^=product-price] > .price::text').get()
        return re.findall('^\d+,\d+', price)[0] if price else None

    def extract_color(self, colors_json, available_color_id):
        for color_json in colors_json:
            if color_json["id"] == available_color_id:
                return color_json["label"]

    def extract_size(self, sizes_json, available_size_id):
        for size_json in sizes_json:
            if size_json["id"] == available_size_id:
                return size_json["label"]

    def extract_color_size_ids(self, attributes_json):
        color_id = ""
        size_id = ""
        for attribute in attributes_json:
            attribute_json = attributes_json[attribute]
            if attribute_json["code"] == "color":
                color_id = attribute_json["id"]
            elif attribute_json["code"] == "pitalia_size":
                size_id = attribute_json["id"]
        return color_id, size_id

    def extract_available_color_size(self, sku_json_script, index):
        color_id, size_id = self.extract_color_size_ids(sku_json_script['attributes'])
        available_size_id = sku_json_script["index"][index][size_id]
        available_color_id = sku_json_script["index"][index][color_id]
        return size_id, color_id, available_size_id, available_color_id

    def extract_sku_features(self, sku_json_script, index):
        size_id, color_id, available_s_id, available_c_id = self.extract_available_color_size(sku_json_script, index)
        sku_item = SkuItem()
        sku_item['price'] = sku_json_script["optionPrices"][index]["finalPrice"]["amount"]
        sku_item['currency'] = "EUR"
        sku_item['previous_price'] = sku_json_script["optionPrices"][index]["oldPrice"]["amount"]
        sku_item['size'] = self.extract_size(sku_json_script["attributes"][size_id]["options"], available_s_id)
        sku_item['color'] = self.extract_size(sku_json_script["attributes"][color_id]["options"], available_c_id)
        return sku_item

    def extract_json_script(self, response):
        json_x = response.xpath('//script[@type="text/x-magento-init" and contains(text(), "jsonConfig")]/text()')
        required_script = {}
        if json_x:
            json_script = json.loads(json_x.get())
            required_script = json_script["[data-role=swatch-options]"]["Magento_Swatches/js/SwatchRenderer"]["jsonConfig"]
        return required_script

    def generate_skus(self, response):
        generated_skus = {}
        sku_json_script = self.extract_json_script(response)
        if sku_json_script:
            skus_index = sku_json_script["index"]
            for index in skus_index.keys():
                generated_skus[index] = self.extract_sku_features(sku_json_script, index)
        return generated_skus

    def extract_image_urls(self, response):
        images_x = response.xpath(
            '//script[@type="text/x-magento-init" and contains(text(), "ThumbSlider")]/text()')
        images_script = images_x.get()
        images_script_json = json.loads(images_script)
        images_urls = images_script_json["[data-gallery-role=bitbull-gallery]"]["Bitbull_ImageGallery/js/bitbullGallery"]["data"]
        return [image_urls["full"] for image_urls in images_urls]

    def extract_care(self, response):
        return response.css('.col.data::text').getall()[-1:]

    def extract_description(self, response):
        return response.css('.product.attibute.description p::text').getall()

    def extract_prod_name(self, response):
        return response.css('.base::text').get()

    def extract_category(self, response):
        categories = response.css('.breadcrumbs li a::text, .breadcrumbs li strong::text').getall()
        return [category.strip() for category in categories]

    def extract_gender(self, response):
        gender_urls = response.meta.get('trail', ['https://www.piazzaitalia.it/'])
        for gender_url in gender_urls:
            if 'donna' in gender_url:
                return 'woman'
            elif 'uomo' in gender_url:
                return 'man'
            elif 'kids' in gender_url:
                return 'kid'
            else:
                return 'not defined'

    def extract_trail(self, response):
        trail_urls = response.meta.get('trail', ['https://www.piazzaitalia.it/'])
        trails = []
        for trail_url in trail_urls:
            name = trail_url.split("/")[-1]
            trails.append([name.split('.')[0], trail_url])
        return trails

    def extract_retailer_sku(self, response):
        return response.css('.price-box.price-final_price::attr(data-product-id)').get()
