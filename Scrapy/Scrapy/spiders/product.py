import scrapy
import json
import re


class ProductSpider(scrapy.Spider):
    name = 'product'

    def start_requests(self):
        url = 'https://www.apc-us.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        listing_css = response.css('.item .go_page::attr(href)')
        product_css = response.css('.item::attr(href)')
        pagination_css = response.css('.pagination a::attr(href)')

        for url in listing_css.getall():
            yield response.follow(url, callback=self.parse)

        for url in product_css.getall():
            yield response.follow(url, callback=self.fetch_item_details)

        for url in pagination_css.getall():
            yield response.follow(url, callback=self.parse)

    def fetch_item_details(self, response):
        product = self.get_script_json(response)
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
        return re.sub('<.*?>', '', product['description']).split('. ')

    def get_image_urls(self, response):
        return ['https:{}'.format(re.sub(r"^\s+", "", img.split(",")[-1])) for img in response.css
                ('[data-zoom-img]::attr(srcset)').getall()]

    def get_script_json(self, response):
        return json.loads(response.css('script[data-product-json]::text').get())

    def get_gender(self, product):
        gender_attribute = [attribute for attribute in product['tags'] if 'Gender' in attribute]
        if gender_attribute:
            return re.split('\\bGender:\\b', gender_attribute[0])[-1]

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
        return variant['compare_at_price'] if variant['compare_at_price'] is list else [variant['compare_at_price']]

    def get_currency(self, response):
        return response.css('[data-currency]::attr(data-currency)').get()
