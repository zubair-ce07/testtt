import json
from urllib.parse import urljoin

from scrapy.spiders import Spider


class ProductParser(Spider):
    ids_seen = set()
    name = 'championStoreSpider'

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
            'retailer': '',
            'name': self.product_name(response),
            'description': self.product_description(response, retailer_sku_id),
            'care': self.product_care(response),
            'image_urls': self.product_image_urls(response.url, available_products),
            'skus': self.product_skus(available_products),
            'price': self.product_price(response),
            'currency': self.product_currency(response)
        }

        return item

    def retailer_sku_id(self, response):
        return response.xpath("//meta[@name='pageId']").css('::attr(content)').get()

    def product_gender(self, response):
        return response.css('#widget_breadcrumb li:nth-child(2)::text').get()

    def product_category(self, response):
        raw_category = response.css('#widget_breadcrumb *::text').getall()
        raw_category = self.remove_unwanted_spaces(raw_category)
        return self.remove_empty_or_unwanted_strings(raw_category)

    def product_name(self, response):
        return response.css('.main_header::text').get()

    def product_description(self, response, retailer_sku_id):
        raw_description = response.css(f'#product_longdescription_{retailer_sku_id} li::text').getall()
        raw_description = self.remove_unwanted_spaces(raw_description)
        return self.remove_empty_or_unwanted_strings(raw_description)

    def product_care(self, response):
        raw_care = response.css('.description ul')[1].css('::text').getall()
        raw_care = self.remove_unwanted_spaces(raw_care)
        return self.remove_empty_or_unwanted_strings(raw_care)

    def product_image_urls(self, response_url, product_skus):
        image_urls = []
        for sku in product_skus:
            for image_url in sku.get('ItemAngleFullImage', []):
                if image_url not in image_urls:
                    image_urls.append(urljoin(response_url, image_url))
        return image_urls

    def product_skus(self, raw_skus):
        product_skus = []

        def sku_color(raw_sku):
            color_key = raw_sku.keys()
            return color_key
            # return color_key.replace('Size_|_', '')

        def sku_size(raw_sku):
            size_key = raw_sku.keys()
            return size_key
            # return size_key.replace('Colour_|_', '')

        for sku in raw_skus:
            product_skus.append(
                {
                    "price": '',
                    "currency": '',
                    "previous_prices": [],
                    "colour": sku_color(sku.get('Attributes')),
                    "size": sku_size(sku.get('Attributes')),
                    "sku_id": sku.get('catentry_id')
                }
            )
        return product_skus

    def product_price(self, response):
        return response.xpath("//meta[@property='og:price:amount']").css('::attr(content)').get()

    def product_currency(self, response):
        return response.xpath("//meta[@property='og:price:currency']").css('::attr(content)').get()

    def product_sku_details(self, response, retailer_sku_number):
        return response.css(f'#entitledItem_{retailer_sku_number}::text').get()

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

    def remove_empty_or_unwanted_strings(self, raw_data):
        clean_data = []
        for data in raw_data:
            if data != '' and data != '/':
                clean_data.append(data)
        return clean_data
