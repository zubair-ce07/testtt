from urllib.parse import urljoin

from scrapy.spiders import Spider

from .productskus import ProductSku
from .utils import (
    clean_string_and_make_json,
    GENDERS,
    remove_empty_strings_or_unwanted_characters,
    remove_unwanted_spaces,
    remove_unicode_characters,
    product_currency,
    product_price)


class ProductParser(Spider):
    ids_seen = set()
    product_sku = ProductSku()
    start_urls = ['https://www.championstore.com/en/champion/collaborations/men--1/champion-x-mlb/new-york-mlb-cooperstown-collection-reverse-weave-hoodie']
    name = 'championStoreSpider'

    def parse(self, response):
        # trail_urls = response.meta['trail']
        trail_urls = []
        retailer_sku_id = self.retailer_sku_id(response)
        if retailer_sku_id in self.ids_seen:
            return

        self.ids_seen.add(retailer_sku_id)
        trail_urls.append(response.url)
        product_details = self.product_sku_details(response, retailer_sku_id)
        products_skus_in_json_form = clean_string_and_make_json(product_details)
        available_products = self.filter_available_products(products_skus_in_json_form)

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
            'image_urls': self.product_image_urls(response.url, available_products),
            'skus': self.product_sku.collect_product_skus(response, available_products, retailer_sku_id),
            'price': product_price(response, retailer_sku_id),
            'currency': product_currency(response)
        }

        return self.product_care(response, item)

    def retailer_sku_id(self, response):
        return response.xpath("//meta[@name='pageId']").css('::attr(content)').get()

    def product_sku_details(self, response, retailer_sku_number):
        return response.css(f'#entitledItem_{retailer_sku_number}::text').get()

    def product_gender(self, response):
        raw_gender_txt = response.css('#widget_breadcrumb *::text').getall()
        for gender in raw_gender_txt:
            if gender in GENDERS:
                return gender.lower()
        return 'both'

    def product_category(self, response):
        raw_category = response.css('#widget_breadcrumb *::text').getall()
        raw_category = remove_unwanted_spaces(raw_category)
        return remove_empty_strings_or_unwanted_characters(raw_category)[1:]

    def product_name(self, response):
        return response.css('.main_header::text').get()

    def product_description(self, response, sku_id):
        raw_description = response.css(f'#product_longdescription_{sku_id} li::text').getall()
        raw_description = remove_unwanted_spaces(raw_description)
        raw_description = remove_unicode_characters(raw_description)
        return remove_empty_strings_or_unwanted_characters(raw_description)

    def product_care(self, response, item):
        raw_care = response.css('.description ul').css('::text').getall()
        raw_care = remove_unwanted_spaces(raw_care)
        raw_care = remove_empty_strings_or_unwanted_characters(raw_care)
        raw_care = remove_unicode_characters(raw_care)
        item['care'] = [care for care in raw_care if care not in item.get('description', [])]
        return item

    def product_image_urls(self, response_url, product_skus):
        image_urls = []

        for sku in product_skus:
            for _, image_url in sku.get('ItemAngleFullImage', {}).items():
                complete_image_url = urljoin(response_url, image_url)

                if complete_image_url not in image_urls:
                    image_urls.append(complete_image_url)

        return image_urls

    def filter_available_products(self, raw_products):
        available_items = []

        for product in raw_products:
            if product.get('available') == 'true':
                available_items.append(product)
        return available_items
