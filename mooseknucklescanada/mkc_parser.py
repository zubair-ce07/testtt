import json
import re

from scrapy.spiders import Spider

from mooseknucklescanada.items import MKCItem


class MKCParser(Spider):
    market = 'CA'
    currency = 'CAD'
    name = 'mkcparser'
    brand = 'mooseknuckles'
    json_pattern = r'\{.*\}'
    retailer = 'mooseknuckles-ca'
    genders = [
        ('women', 'women'),
        ('woman', 'women'),
        ('ladies', 'women'),
        ('boy', 'boys'),
        ('boys', 'boys'),
        ('girl', 'girls'),
        ('girls', 'girls'),
        ('man', 'men'),
        ('men', 'men'),
        ('mens', 'men'),
        ('adults', 'unisex-adults'),
        ('kids', 'unisex-kids'),
    ]

    def parse(self, response):
        item = MKCItem()
        item['brand'] = self.brand
        item['url'] = response.url
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['name'] = self.get_name(response)
        item['care'] = self.get_care(response)
        item['gender'] = self.get_gender(response)
        item['trail'] = response.meta.get('trail', [])
        item['category'] = self.get_categories(response)
        item['image_urls'] = self.get_image_urls(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['description'] = self.get_description(response)
        item['skus'] = self.get_skus(response)

        return item

    def get_name(self, response):
        return response.css('.product-name h1::text').get()

    def get_gender(self, response):
        gender_candidate = response.css('.std::text').get().lower()

        for tag, gender in self.genders:
            if tag in gender_candidate:
                return gender

        return 'unisex-adults'

    def get_care(self, response):
        care_css = '#collateral-tabs .tab-container:nth-child(4) .tab-content li::text'
        return self.sanitize_list(response.css(care_css).getall())

    def get_categories(self, response):
        categories = response.css('.std::text').getall()
        categories.append(response.css('button.btn-cart::attr(data-category)').get())

        return self.sanitize_list(categories)

    def get_image_urls(self, response):
        return response.css('.product-image-gallery img::attr(data-src)').getall()

    def get_product_id(self, response):
        return response.css('meta[property="product:retailer_item_id"]::attr(content)').get()

    def get_description(self, response):
        return self.sanitize_list(response.css('.tab-content .std::text').getall())

    def get_skus(self, response):
        skus = []
        out_of_stock = self.get_out_of_stock(response)
        if out_of_stock:
            return skus

        return self.get_colour_size_skus(response, out_of_stock)

    def get_colour_size_skus(self, response, out_of_stock):
        skus = []
        attributes_json = response.css('#product-options-wrapper script').re_first(self.json_pattern)
        attributes_json = json.loads(attributes_json)['attributes']
        raw_colour_skus, raw_size_skus = attributes_json['141']['options'], attributes_json['142']['options']
        pricing_details = self.get_pricing_details(response)

        for raw_colour_sku in raw_colour_skus:

            for product in raw_colour_sku['products']:

                for raw_size_sku in raw_size_skus:

                    if product in raw_size_sku['products']:
                        sku = {**pricing_details, 'size': raw_size_sku['label'], 'colour': raw_colour_sku['label']}
                        sku['out_of_stock'] = out_of_stock
                        sku['sku_id'] = f'{sku["colour"]}_{sku["size"]}'
                        skus.append(sku)
                        break

        return skus

    def get_out_of_stock(self, response):
        out_of_stock = response.css('meta[property="product:availability"]::attr(content)').get()
        return False if out_of_stock == 'in stock' else True

    def get_pricing_details(self, response):
        pricing_json = response.css('div.main script').re_first(self.json_pattern)
        pricing_json = json.loads(pricing_json)
        pricing = {'currency': self.currency}
        pricing['price'] = self.sanitize_price(pricing_json['productPrice'])
        pricing['previous_prices'] = [self.sanitize_price(pricing_json['productOldPrice'])]

        return pricing

    def sanitize_price(self, price, to_cents=True):
        final_price = price

        if isinstance(final_price, str):
            final_price = float(''.join(re.findall(r'\d+', final_price)))
        if to_cents:
            final_price *= 100

        return final_price

    def sanitize_list(self, inputs):
        return list(map(lambda i: i and i.strip(), inputs))
