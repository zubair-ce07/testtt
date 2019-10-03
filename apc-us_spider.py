import scrapy
import json


class ApcSpider(scrapy.Spider):
    name = 'apc-us'
    start_urls = [
        'https://www.apc-us.com',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
    }

    def parse(self, response):
        navigation_links = response.css('.nav-primary-item a::attr(href)').getall()
        meta = {'dont_merge_cookies': True}
        for url in navigation_links:
            listing_url = response.urljoin(url)
            yield scrapy.Request(url=listing_url,
                                 callback=self.parse_products_url,
                                 meta=meta)

    def parse_products_url(self, response):
        product_links = response.css('a.item::attr(href)').getall() \
                        or response.css('.colorama-product-link-wrapper::attr(href)').getall()
        for product_url in product_links:
            listing_url = response.urljoin(product_url)
            yield scrapy.Request(url=listing_url,
                                 callback=self.parse_detail_page_info,
                                 meta=response.meta)

    def get_product_category(self, response, json_response):
        product_category = []
        product_category.extend([response.meta['gender'], json_response['type']])
        return product_category

    def get_all_variants(self, json_response, product_price, product_currency):
        product_variants_sku = []
        for variant in json_response['variants']:
            product_variants_sku.extend([
                                         {'sku_id': variant['sku'],
                                          'color': variant['option1'],
                                          'currency': product_currency,
                                          'size': variant['option2'],
                                          'out_of_stock': not variant['available'],
                                          'price': product_price,
                                          'previous_price': product_price}
                                        ])
        return product_variants_sku

    def parse_detail_page_info(self, response):
        url = '{}.js' .format(response.url.split('?')[0])
        response.meta['product_price'] = response.css('span#variantPrice::text').get().strip('$')
        response.meta['product_currency'] = \
            response.css('meta#in-context-paypal-metadata::attr(data-currency)').get()
        response.meta['url'] = response.url
        response.meta['gender'] = response.css('nav span.has-separator a::text').get()
        yield scrapy.Request(url=url, callback=self.parse_product_api,
                             meta=response.meta)

    def parse_product_api(self, response):
        json_response = json.loads(response.text)
        product_price = response.meta['product_price']
        product_currency = response.meta['product_currency']
        product_variants_sku = self.get_all_variants(json_response, product_price, product_currency)
        product_category = self.get_product_category(response, json_response)
        prod_desc_from_response = json_response['description']
        product_description = prod_desc_from_response.replace('<p>', '').replace('</p>', '')

        yield {
            'product_name': json_response['title'],
            'category': product_category,
            'description': product_description,
            'image_urls': json_response['images'],
            'brand': 'A.P.C',
            'retailer_sku': json_response['id'],
            'url': response.meta['url'],
            'skus': product_variants_sku,
            'gender': response.meta['gender'],
        }
 