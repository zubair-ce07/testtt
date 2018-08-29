import json
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
        product['skus'] = self.generate_skus(response)
        product['price'] = self.product_price(response)
        product['spider_name'] = self.name
        return product

    def product_id(self, response):
        return response.css('.price-final_price::attr(data-product-id)').extract_first()

    def product_trail(self, response):
        trail_urls = response.meta.get('trail', ['https://www.piazzaitalia.it/'])
        return [[url.split("/")[-1].split(".")[0], url] for url in trail_urls]

    def product_gender(self, response):
        gender_map = {'donna': 'women', 'uomo': 'men', 'kids': 'unisex-kids'}
        soup = ' '.join(response.meta.get('trail', []) + response.css('.breadcrumbs *::attr(href)').extract())
        for gender in gender_map:
            if gender in soup:
                return gender_map[gender]
        return 'unisex-adults'

    def product_category(self, response):
        categories = response.css('.breadcrumbs a::text').extract()
        return [category.strip() for category in categories if category]

    def product_name(self, response):
        return response.css('.base::text').extract_first()

    def product_description(self, response):
        return response.css('.description p::text').extract()

    def product_care(self, response):
        return response.css('.col.data::text').extract()[-1:]

    def image_urls(self, response):
        raw_images = response.xpath('//script[contains(text(), "ThumbSlider")]/text()').extract_first()
        raw_images = json.loads(raw_images)
        image_urls = raw_images["[data-gallery-role=bitbull-gallery]"]["Bitbull_ImageGallery/js/bitbullGallery"]["data"]
        return [url["full"] for url in image_urls]

    def generate_skus(self, response):
        skus = {}
        raw_skus = self.product_details(response)
        if raw_skus:
            product_data = self.map_attributes(raw_skus)
            common_sku = self.product_pricing(response)
            for sku_id in raw_skus["index"].keys():
                sku = common_sku.copy()
                sku['size'] = product_data[sku_id]["pitalia_size"]
                sku['color'] = product_data[sku_id]["color"]
                skus[sku_id] = sku
        return skus

    def product_details(self, response):
        p_info = response.xpath('//script[contains(text(), "jsonConfig")]/text()').extract_first()
        p_info = json.loads(p_info or '{}')
        return p_info["[data-role=swatch-options]"]["Magento_Swatches/js/SwatchRenderer"]["jsonConfig"] if p_info else {}

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
        return response.css('.product-info-price ::attr(data-price-amount)').extract_first()

    def product_pricing(self, response):
        pricing = {}
        pricing['price'] = self.product_price(response)
        pricing['old_price'] = response.css('[id^=old-price]::attr(data-price-amount)').extract_first()
        pricing['currency'] = 'EUR'
        return pricing
