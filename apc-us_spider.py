from scrapy import Spider, Selector
import json


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
        for navigation_link in response.css('.nav-primary-item a'):
            yield response.follow(navigation_link,
                                  callback=self.parse_product_page_links,
                                  meta=meta)

    def parse_product_page_links(self, response):
        for product_link in response.css('.colorama-product-link-wrapper' or
                                         'a.item'):
            yield response.follow(product_link,
                                  callback=self.parse_detail_page_info,
                                  meta=response.meta)

    def get_category(self, response, raw_product):
        category = []
        category.extend([response.meta['gender'], raw_product['type']])
        return category

    def get_all_variants(self, raw_products, price, currency):
        variants_sku = []
        for raw_product in raw_products['variants']:
            variants_sku.append(
                                {'sku_id': raw_product['sku'],
                                 'color': raw_product['option1'],
                                 'currency': currency,
                                 'size': raw_product['option2'],
                                 'out_of_stock': not raw_product['available'],
                                 'price': price,
                                 'previous_price': price}
            )
        return variants_sku

    def parse_detail_page_info(self, response):
        url = '{}.js'.format(response.url.split('?')[0])
        response.meta['price'] = response.css('span#variantPrice::text') \
            .get().strip('$')
        response.meta['currency'] = \
            response.css('meta#in-context-paypal-metadata::attr(data-currency)') \
            .get()
        response.meta['url'] = response.url
        response.meta['gender'] = response.css('nav span.has-separator a::text') \
            .get()
        yield response.follow(url, callback=self.parse_api,
                              meta=response.meta)

    def parse_api(self, response):
        raw_product = json.loads(response.text)
        price = response.meta['price']
        currency = response.meta['currency']
        variants_sku = self.get_all_variants(raw_product, price, currency)
        category = self.get_category(response, raw_product)
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
               'url': response.meta['url'],
               'skus': variants_sku,
               'gender': response.meta['gender'],
        }
