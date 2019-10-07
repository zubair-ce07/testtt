from scrapy import Spider, Selector
import json
from urllib.parse import urlparse


class ApcSpider(Spider):
    name = 'apc-us'
    start_urls = [
        'https://www.apc-us.com',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
    }

    def parse(self, response):
        meta = {'dont_merge_cookies': True}
        for product_listing in response.css('.nav-primary-item a'):
            yield response.follow(product_listing,
                                  callback=self.parse_products_link,
                                  meta=meta)

    def parse_products_link(self, response):
        for product_link in response.css('.colorama-product-link-wrapper, \
                                         a.item'):
            yield response.follow(product_link,
                                  callback=self.parse_product_details,
                                  meta=response.meta)

    def get_categories(self, response, raw_product):
        return [response.meta['required_details']['gender'],
                raw_product['type']]

    def get_skus(self, raw_product, price, currency):
        skus = []
        for variant in raw_product['variants']:
            skus.append(
                        {'sku_id': variant['sku'],
                         'color': variant['option1'],
                         'currency': currency,
                         'size': variant['option2'],
                         'out_of_stock': not variant['available'],
                         'price': price,
                         'previous_price': price}
            )
        return skus

    def parse_product_details(self, response):
        url = '{}.js'.format(urlparse(response.url).path)
        currency = response.css('meta#in-context-paypal-'
                                'metadata::attr(data-currency)').get()
        price = response.css('span#variantPrice::text') \
            .get().strip('$')
        gender = response.css('nav span.has-separator a::text').get()
        response.meta['required_details'] = {
            'price': price,
            'currency': currency,
            'url': response.url,
            'gender': gender
        }
        yield response.follow(url, callback=self.parse_product_api,
                              meta=response.meta)

    def parse_product_api(self, response):
        raw_product = json.loads(response.text)
        price = response.meta['required_details']['price']
        currency = response.meta['required_details']['currency']
        skus = self.get_skus(raw_product, price, currency)
        category = self.get_categories(response, raw_product)
        desc_from_response = raw_product['description']
        description_selector = Selector(text=desc_from_response)
        description = description_selector.css('p::text').get()
        yield {
               'product_name': raw_product['title'],
               'category': category,
               'description': description,
               'image_urls': raw_product['images'],
               'brand': 'A.P.C',
               'retailer_sku': raw_product['id'],
               'url': response.meta['required_details']['url'],
               'skus': skus,
               'gender': response.meta['required_details']['gender'],
        }
