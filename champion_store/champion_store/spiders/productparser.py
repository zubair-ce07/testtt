from urllib.parse import urljoin

from scrapy.spiders import Spider

from .productskus import ProductSku
from .utils import *
from ..items import Product


class ProductParser(Spider):
    ids_seen = set()
    product_sku = ProductSku()
    name = 'championStoreSpider'

    def parse(self, response):
        retailer_sku_id = self.retailer_sku_id(response)
        if retailer_sku_id in self.ids_seen:
            return

        self.ids_seen.add(retailer_sku_id)

        trail_urls = response.meta['trail']
        trail_urls.append(response.url)

        raw_product_details = self.product_sku_details(response, retailer_sku_id)
        products_skus = clean_string(raw_product_details)

        available_products = self.filter_available_products(products_skus)
        item = Product()

        item['retailer_sku'] = retailer_sku_id
        item['trail'] = trail_urls
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['brand'] = 'champion store'
        item['url'] = response.url
        item['market'] = 'UK'
        item['retailer'] = 'ChampionStore-UK'
        item['name'] = self.product_name(response)
        item['description'] = self.product_description(response, retailer_sku_id)
        item['image_urls'] = self.product_image_urls(response.url, available_products)
        item['skus'] = self.product_sku.collect_product_skus(response, available_products, retailer_sku_id)
        item['price'] = self.product_price(response, retailer_sku_id)
        item['currency'] = self.product_currency(response)

        item = self.product_care(response, item)
        yield item

    def retailer_sku_id(self, response):
        return response.css('meta[name="pageId"]::attr(content)').get()

    def product_sku_details(self, response, retailer_sku_number):
        return response.css(f'#entitledItem_{retailer_sku_number}::text').get()

    def product_gender(self, response):
        raw_genders = response.css('#widget_breadcrumb *::text').getall()
        for gender in raw_genders:
            if gender in GENDERS:
                return gender.lower()
        return 'unisex'

    def product_category(self, response):
        raw_category = response.css('#widget_breadcrumb *::text').getall()
        raw_category = remove_unwanted_spaces(raw_category)
        return remove_unwanted_characters(raw_category)[1:]

    def product_name(self, response):
        return response.css('.main_header::text').get()

    def product_description(self, response, sku_id):
        raw_description = response.css(f'#product_longdescription_{sku_id} li::text').getall()
        raw_description = remove_unwanted_spaces(raw_description)
        raw_description = remove_unicode_characters(raw_description)
        return remove_unwanted_characters(raw_description)

    def product_care(self, response, item):
        raw_care = response.css('.description ul').css('::text').getall()
        raw_care = remove_unwanted_spaces(raw_care)
        raw_care = remove_unwanted_characters(raw_care)
        raw_care = remove_unicode_characters(raw_care)
        item['care'] = [care for care in raw_care if care not in item.get('description', [])]
        return item

    def product_image_urls(self, response_url, product_skus):
        image_urls = []

        for sku in product_skus:
            for image_url in sku.get('ItemAngleFullImage', {}).values():
                complete_image_url = urljoin(response_url, image_url)

                if complete_image_url not in image_urls:
                    image_urls.append(complete_image_url)

        return image_urls

    def product_price(self, response, sku_id):
        raw_price = response.css(f'#ProductInfoPrice_{sku_id} ::attr(value)').re_first(r'[\d.]+')
        return raw_price.replace('.', '')

    def product_currency(self, response):
        return response.xpath("//meta[@property='og:price:currency']").css('::attr(content)').get()

    def filter_available_products(self, raw_products):
        available_items = []

        for product in raw_products:
            if product.get('available') == 'true':
                available_items.append(product)
        return available_items
