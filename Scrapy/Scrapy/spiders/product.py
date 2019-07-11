import scrapy
import json
import re


class ProductSpider(scrapy.Spider):
    name = 'product'
    start_urls = ['https://www.apc-us.com/']

    def parse(self, response):
        listing_css = '.item .go_page::attr(href)'
        product_css = '.item::attr(href)'
        pagination_css = '.pagination a::attr(href)'

        for url in response.css(listing_css).getall():
            yield response.follow(url, callback=self.parse)

        for url in response.css(product_css).getall():
            yield response.follow(url, callback=self.parse_product)

        for url in response.css(pagination_css).getall():
            yield response.follow(url, callback=self.parse)

    def parse_product(self, response):
        product = self.get_raw_product(response)
        return {
            'name': product['title'],
            'category': self.get_category(response),
            'description':  self.get_description(product),
            'image_urls': self.get_image_urls(response),
            'brand':  'A.P.C',
            'retailer_sku': product['id'],
            'url': response.url,
            'gender': self.get_gender(product),
            'skus': self.get_skus(response, product)
        }

    def get_category(self, response):
        return response.css('.breadcrumbs a::text').getall()

    def get_description(self, product):
        description = scrapy.selector.Selector(text=product["description"])
        return [desc.strip() for desc in description.css("::text").getall() if desc.strip()]

    def get_image_urls(self, response):
        return ['https:{}'.format(img) for img in response.css('.desktop-product-img::attr(data-zoom-img)').getall()]

    def get_raw_product(self, response):
        return json.loads(response.css('script[data-product-json]::text').get())

    def get_gender(self, product):
        gender_attr = [attribute for attribute in product['tags'] if 'Gender' in attribute]
        if gender_attr:
            return re.findall(r'^Gender:(\w+)$', gender_attr[0])[0]

    def get_skus(self, response, product):
        skus = []
        for variant in product['variants']:
            skus.append({
                'sku_id': variant['id'],
                'color': variant['option1'],
                'currency': self.get_currency(response),
                'size': variant['option2'],
                'out_of_stock': not variant['available'],
                'price': variant['price'],
                'previous_price': self.get_prev_price(variant)
            })
        return skus

    def get_prev_price(self, variant):
        return variant['compare_at_price'] if type(variant['compare_at_price']) is list \
            else [variant['compare_at_price']]

    def get_currency(self, response):
        return response.css('[data-currency]::attr(data-currency)').get()
