import json
import re
from scrapy import Spider
from piazza.items import ProductItem


class ProductParser(Spider):
    name = "piazza-parse"

    def parse(self, response):
        product = ProductItem(brand="Piazzaitalia", market="IT", retailer='piazzaitalia-it', currency="EUR")
        product['retailer_sku'] = self.product_id(response)
        product['trail'] = self.product_trail(response)
        product['gender'] = self.product_gender(response)
        product['category'] = self.product_category(response)
        product['url'] = response.url
        product['name'] = self.product_name(response)
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['image_urls'] = self.image_urls(response)
        product['skus'] = self.raw_skus(response)
        product['price'] = self.product_price(response)
        product['spider_name'] = self.name
        return product

    def product_id(self, response):
        return response.css('.price-box.price-final_price::attr(data-product-id)').extract_first()

    def product_trail(self, response):
        trail_urls = response.meta.get('trail', ['https://www.piazzaitalia.it/'])
        return [[url.split("/")[-1].split(".")[0], url] for url in trail_urls]

    def product_gender(self, response):
        possible_genders = {'donna': 'women', 'uomo': 'men', 'kids': 'kids'}
        gender_urls = response.meta.get('trail', ['https://www.piazzaitalia.it/'])
        gender_urls.extend(response.css('.breadcrumbs *::attr(href)').extract())
        for url in gender_urls:
            gender = re.findall('(donna|uomo|kids)', url)
            if gender:
                return possible_genders[gender[0]]
        return 'unisex'

    def product_category(self, response):
        categories = response.css('.breadcrumbs *::text').extract()
        filtered_categories = [category.strip() for category in categories]
        return list(filter(None, filtered_categories))

    def product_name(self, response):
        return response.css('.base::text').extract_first()

    def product_description(self, response):
        return response.css('.product.attibute.description p::text').extract()

    def product_care(self, response):
        return response.css('.col.data::text').extract()[-1:]

    def image_urls(self, response):
        raw_images = response.xpath('//script[contains(text(), "ThumbSlider")]/text()').extract_first()
        raw_images = json.loads(raw_images)
        image_urls = raw_images["[data-gallery-role=bitbull-gallery]"]["Bitbull_ImageGallery/js/bitbullGallery"]["data"]
        return [url["full"] for url in image_urls]

    def raw_skus(self, response):
        skus = {}
        product_data_ = self.product_details(response)
        if product_data_:
            product_data = self.map_attributes(product_data_)
            skus_index = product_data_["index"]
            for index in skus_index.keys():
                price = product_data_["optionPrices"][index]["finalPrice"]["amount"]
                old_price = product_data_["optionPrices"][index]["oldPrice"]["amount"]
                size = product_data[index]["pitalia_size"]
                color = product_data[index]["color"]
                skus[index] = {'price': price, 'currency': 'EUR', 'old_price': old_price, 'size': size, 'color': color}
        return skus

    def product_details(self, response):
        product_info = response.xpath('//script[contains(text(), "jsonConfig")]/text()').extract_first()
        attributes = {}
        if product_info:
            product_info = json.loads(product_info)
            attributes = product_info["[data-role=swatch-options]"]["Magento_Swatches/js/SwatchRenderer"]["jsonConfig"]
        return attributes

    def map_attributes(self, product_data):
        attributes = product_data["attributes"]
        product_sku = {}
        for feat_value in attributes.values():
            feature = feat_value["code"]
            for option in feat_value["options"]:
                for product in option["products"]:
                    if product not in product_sku.keys():
                        product_sku[product] = {}
                    product_sku[product][feature] = option["label"]
        return product_sku

    def product_price(self, response):
        return response.css('.product-info-price *::attr(data-price-amount)').extract_first()
