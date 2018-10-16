import re
import js2py
import datetime

from alcott.items import Product


class ProductParser():
    name = 'alcott-parser'

    def parse(self, response):
        item = Product()

        item['retailer_sku'] = self.product_retailer_sku(response)
        item['trail'] = self.product_trail(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['brand'] = 'Alcott'
        item['url'] = response.url
        item['date'] = str(datetime.date.today())
        item['market'] = 'EU'
        item['retailer'] = 'Alcott-EU'
        item['url_original'] = response.url
        item['name'] = self.product_name(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.product_image_urls(response)
        item['skus'] = self.product_skus(response)

        yield item

    def product_retailer_sku(self, response):
        raw_sku = response.css('.sku::text').extract_first()
        retailer_sku = raw_sku.split(':')[-1]
        return retailer_sku

    def product_trail(self, response):
        return response.css('[property*=url]::attr(content)').extract()

    def product_gender(self, response):
        css = '#widget_breadcrumb li:nth-child(2) a::text'
        gender = response.css(css).extract_first()
        return gender.strip() if gender else 'unisex-adults'

    def product_category(self, response):
        css = '#widget_breadcrumb li:nth-last-child(2) a::text'
        category = response.css(css).extract_first()
        return str(category).strip()

    def product_name(self, response):
        return response.css('.main_header::text').extract_first()

    def product_care(self, response):
        raw_care = response.css('#itemCareList span::text').extract()
        return [care.strip() for care in raw_care]

    def product_image_urls(self, response):
        items = self.extract_data(response)
        return [self.extract_images(item['PhotoGallery']) for item in items]

    def product_skus(self, response):
        raw_items = self.extract_data(response)
        items = [self.extract_attributes(item['Attributes'])
                 for item in raw_items]

        skus = {}
        for item in items:
            sku = {}
            sku['color'] = list(item.keys())[0]
            sku['size'] = list(item.values())[0]
            sku['price'] = self.product_price(response)
            sku['currency'] = self.product_currency(response)
            unique_id = '{}_{}'.format(sku['color'], sku['size'])
            skus.update({unique_id: sku})
        return skus

    def extract_data(self, response):
        css = '[id*=entitledItem]::text'
        raw_items = response.css(css).extract_first()
        items = js2py.eval_js(raw_items)
        return items

    def extract_images(self, products):
        return [product['base'] for product in products]

    def extract_attributes(self, raw_attributes):
        attributes = raw_attributes.keys()
        attributes = [attribute.split('_|_')[-1] for attribute in attributes]

        return {attributes[index]: attributes[index + 1]
                for index in range(0, len(attributes), 2)}

    def chunks(self, data, index):
        for i in range(0, len(data), index):
            yield data[i:i+index]

    def product_price(self, response):
        raw_price = response.css('.price::text').extract_first()
        price = re.sub(r'\D', '', raw_price)
        return price

    def product_currency(self, response):
        raw_currency = response.css('.price::text').extract_first()
        currency = re.sub(r'[\d.]', '', raw_currency)
        return currency.strip()
