import re
import datetime

from scrapy import Spider
from js2py import eval_js

from alcott.items import Product


class ProductParser(Spider):
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
        retailer_sku = re.findall(r':\w*', raw_sku)[0]
        return retailer_sku.replace(':', '')

    def product_trail(self, response):
        return response.css('[property*=url]::attr(content)').extract()

    def product_gender(self, response):
        css = '#widget_breadcrumb li:nth-child(2) a::text'
        gender = response.css(css).extract_first()
        return gender.strip() if gender else 'unisex-adults'

    def product_category(self, response):
        css = '#widget_breadcrumb li::text'
        raw_category = response.css(css).extract()
        category = [c.strip() for c in raw_category]
        return [c for c in category if c != '']

    def product_name(self, response):
        return response.css('.main_header::text').extract_first()

    def product_care(self, response):
        raw_care = response.css('#itemCareList span::text').extract()
        return [c.strip() for c in raw_care]

    def product_image_urls(self, response):
        products = self.product_information(response)
        images = []
        for product in products:
            images += self.product_images(product['PhotoGallery'], response)
        return list(set(images))

    def product_skus(self, response):
        raw_skus = self.product_information(response)
        raw_skus = [self.sku_attributes(sku['Attributes'])
                    for sku in raw_skus]
        skus = {}
        common_sku = {}
        common_sku['price'] = self.product_price(response)
        common_sku['currency'] = self.product_currency(response)

        for raw_sku in raw_skus:
            sku = common_sku.copy()
            sku['color'] = raw_sku['attr0']
            sku['size'] = raw_sku['attr1']
            sku_id = '{}_{}'.format(sku['color'], sku['size'])
            skus.update({sku_id: sku})
        return skus

    def product_information(self, response):
        css = '[id*=entitledItem]::text'
        raw_information = response.css(css).extract_first()
        product_information = eval_js(raw_information)
        return product_information

    def product_images(self, products, response):
        return [response.urljoin(p['base']) for p in products]

    def sku_attributes(self, raw_attributes):
        attributes = raw_attributes.keys()
        attributes = [attribute.split('_|_')[-1] for attribute in attributes]
        return {f'attr{index}': attributes[index]
                for index in range(0, len(attributes))}

    def product_price(self, response):
        raw_price = response.css('.price::text').extract_first()
        price = re.sub(r'\D', '', raw_price)
        return price

    def product_currency(self, response):
        raw_currency = response.css('.price::text').extract_first()
        currency = re.sub(r'[\d.]', '', raw_currency)
        return currency.strip()
