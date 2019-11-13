import json
import re
from urllib.parse import urljoin

from scrapy.spiders import Spider


class ProductParser(Spider):
    ids_seen = set()
    name = 'championStoreSpider'
    VALUE_EXTRACTOR_FROM_KEY = re.compile(r'(?:.*_|_)(.*)')

    def parse(self, response):
        trail_urls = response.meta['trail']
        retailer_sku_id = self.retailer_sku_id(response)
        if retailer_sku_id in self.ids_seen:
            return

        self.ids_seen.add(retailer_sku_id)
        trail_urls.append(response.url)
        product_details = self.product_sku_details(response, retailer_sku_id)
        products_skus_in_json_form = self.clean_string_and_make_json(product_details)
        available_products = self.filter_unavailable_products(products_skus_in_json_form)

        item = {
            'retailer_sku': retailer_sku_id,
            'trail': trail_urls,
            'gender': self.product_gender(response),
            'category': self.product_category(response),
            'brand': 'champion store',
            'url': response.url,
            'market': 'UK',
            'retailer': 'ChampionStore-UK',
            'name': self.product_name(response),
            'description': self.product_description(response, retailer_sku_id),
            'care': self.product_care(response),
            'image_urls': self.product_image_urls(response.url, available_products),
            'skus': self.product_skus(response, available_products, retailer_sku_id),
            'price': self.product_price(response, retailer_sku_id),
            'currency': self.product_currency(response)
        }

        return item

    def retailer_sku_id(self, response):
        return response.xpath("//meta[@name='pageId']").css('::attr(content)').get()

    def product_sku_details(self, response, retailer_sku_number):
        return response.css(f'#entitledItem_{retailer_sku_number}::text').get()

    def product_gender(self, response):
        raw_gender_txt = response.css('#widget_breadcrumb *::text').getall()
        for text in raw_gender_txt:
            if text == 'MEN' or text == 'WOMEN':
                return text
        return 'both'

    def product_category(self, response):
        raw_category = response.css('#widget_breadcrumb *::text').getall()
        raw_category = self.remove_unwanted_spaces(raw_category)
        return self.remove_empty_or_unwanted_characters(raw_category)[1:]

    def product_name(self, response):
        return response.css('.main_header::text').get()

    def product_description(self, response, sku_id):
        raw_description = response.css(f'#product_longdescription_{sku_id} li::text').getall()
        raw_description = self.remove_unwanted_spaces(raw_description)
        return self.remove_empty_or_unwanted_characters(raw_description)

    def product_care(self, response):
        raw_care = response.css('.description ul').css('::text').getall()
        raw_care = self.remove_unwanted_spaces(raw_care)
        return self.remove_empty_or_unwanted_characters(raw_care)

    def product_image_urls(self, response_url, product_skus):
        image_urls = []

        for sku in product_skus:
            for _, image_url in sku.get('ItemAngleFullImage', {}).items():
                if image_url not in image_urls:
                    image_urls.append(urljoin(response_url, image_url))
        return image_urls

    def product_skus(self, response, raw_skus, sku_id):
        product_skus = []

        def clean_key_value(raw_key_value):
            return self.VALUE_EXTRACTOR_FROM_KEY.findall(raw_key_value)

        def sku_color(raw_sku):
            if not raw_skus:
                return 'one'

            color_key = list(raw_sku.keys())[1]
            return clean_key_value(color_key)

        def sku_size(raw_sku):
            if not raw_skus:
                return 'one'

            size_key = list(raw_sku.keys())[0]
            return clean_key_value(size_key)

        def sku_previous_price(response):
            raw_previous_price = response.css(f'#ProductInfoListPrice_{sku_id}::attr(value)').re_first(r'[\d.]+')
            return raw_previous_price.replace('.', '') if raw_previous_price else None

        for sku in raw_skus:
            product_skus.append(
                {
                    "price": '',
                    "currency": '',
                    "previous_prices": [sku_previous_price(response)],
                    "colour": sku_color(sku.get('Attributes')),
                    "size": sku_size(sku.get('Attributes')),
                    "sku_id": sku.get('catentry_id')
                }
            )
        return product_skus

    def product_price(self, response, sku_id):
        raw_price = response.css(f'#ProductInfoPrice_{sku_id} ::attr(value)').re_first(r'[\d.]+')
        return raw_price.replace('.', '')

    def product_currency(self, response):
        return response.xpath("//meta[@property='og:price:currency']").css('::attr(content)').get()

    def filter_unavailable_products(self, raw_products):
        available_items = []

        for product in raw_products:
            if product.get('available') == 'true':
                available_items.append(product)
        return available_items

    def clean_string_and_make_json(self, raw_text):
        raw_text = raw_text.replace('\'', '"')
        return json.loads(raw_text)

    def remove_unwanted_spaces(self, raw_data):
        if type(raw_data) is list:
            return [d.strip() for d in raw_data]
        return raw_data.strip()

    def remove_empty_or_unwanted_characters(self, raw_data):
        clean_data = []
        for data in raw_data:
            if data != '' and data != '/':
                clean_data.append(data)
        return clean_data
