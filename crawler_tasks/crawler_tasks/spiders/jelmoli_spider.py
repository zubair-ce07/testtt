import re
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest, TextResponse
from crawler_tasks.items import JelmoliProduct


class JelmoliSpider(CrawlSpider):
    name = 'jelmoli'
    allowed_domains = ['jelmoli-shop.ch']
    start_urls = [
        'https://www.jelmoli-shop.ch/'
    ]
    unwanted_categories = [
        'marken', 'elektronik', 'spielzeug', 'sportbedarf',
        'fitnessgeraete', 'aktionen', 'werkzeuge', 'sale'
    ]
    rules = (
        Rule(LinkExtractor(
            restrict_css=('.rendered-data', '[class^="sh"]'), deny=unwanted_categories),
            callback='parse_category_url', follow=True),
    )

    words_regex = re.compile('\w+')
    base_url = 'https://www.jelmoli-shop.ch'
    pagination_url = 'https://www.jelmoli-shop.ch/suche/mba/magellan'
    product_page_url_t = 'https://www.jelmoli-shop.ch/p/{}/{}'
    product_skus_url_t = 'https://www.jelmoli-shop.ch/INTERSHOP/rest/WFS/EmpirieCom-JelmoliCH-Site/-;' \
        'loc=de_CH;cur=CHF/inventories/{}/master'

    def parse_category_url(self, response):
        raw_json = response.css('.product-listing-json::text').extract_first()
        if not raw_json:
            return

        pre_known_product_values = {}
        url = response.url

        if 'herren' in url:
            pre_known_product_values['gender'] = 'men'
        elif 'damen' in url:
            pre_known_product_values['gender'] = 'women'
        elif 'kinder' in url:
            pre_known_product_values['gender'] = 'kids'
        elif any(keyword in url for keyword in ['bettwaesche', 'wohnen']):
            pre_known_product_values['industry'] = 'homeware'

        return self.parse_category(raw_json, pre_known_product_values)

    def parse_category(self, raw_json, pre_known_product_values):
        meta = {
            'pre_known_product_values': pre_known_product_values
        }
        request = Request(self.base_url, meta=meta)
        response = TextResponse(url='', body=raw_json.encode(), request=request)
        for product_request in self.parse_product_listing(response):
            yield product_request

        category_detail = json.loads(raw_json)['result']
        category_id = category_detail['category']['current']['id']
        product_count = category_detail['count']
        per_request_count = len(category_detail['styles'])
        requested_count = per_request_count
        payload = {
            'category': category_id,
            'channel': "web",
            'clientId': "JelmoliCh",
            'locale': "de_CH"
        }
        while requested_count < product_count:
            payload['start'] = requested_count
            payload['count'] = per_request_count
            requested_count += per_request_count
            yield FormRequest(
                self.pagination_url, body=json.dumps(payload), meta=meta,
                callback=self.parse_product_listing)

    def parse_product_listing(self, response):
        product_listing = json.loads(response.text)
        items = product_listing.get('searchresult', product_listing)['result']['styles']
        pre_known_product_values = response.meta.get('pre_known_product_values', {})

        product_requests = []
        for item in items:
            try:
                name_without_brand = item['name'].split(' ', 1)[1]
            except IndexError:
                name_without_brand = item['name']

            meta = {
                'product_id': item['masterSku'],
                'name': item.get('nameNoBrand', name_without_brand),
                'brand': item['brand'],
                'description': item['description'],
                'currency': item['price']['currency'],
                'price': item['price']['value'],
                'previous_price': item.get('oldPrice', {}).get('value', ''),
                'pre_known_product_values': pre_known_product_values
            }

            words = self.words_regex.findall(item['name'])
            name = '-'.join([word.lower() for word in words])
            url = self.product_page_url_t.format(name, item['masterSku'])
            product_requests.append(
                Request(url, meta=meta, callback=self.parse_product))
        return product_requests

    def parse_product(self, response):
        meta = response.meta
        product = JelmoliProduct()
        product['merch_info'] = []
        product['market'] = ''
        product['product_id'] = meta['product_id']
        product['name'] = meta['name']
        product['brand'] = meta['brand']
        product['description'] = meta['description']
        product['url'] = response.url
        product['category'] = response.css('.nav-breadcrumb a::text').extract()
        product['care'] = self.parse_product_care(response)
        product.update(response.meta.get('pre_known_product_values', {}))
        product['image_urls'] = self.parse_image_urls(response)

        meta['product'] = product
        url = self.product_skus_url_t.format(meta['product_id'])
        return Request(url, meta=meta, callback=self.parse_skus)

    def parse_product_care(self, response):
        desc1_selector = response.css('[itemprop="description"]')
        if not desc1_selector:
            return []

        desc2 = desc1_selector.css('.oocv-description').extract_first()
        if desc2 and '%' in desc2:
            return [desc2]
        else:
            desc1 = desc1_selector.extract_first()
            if '%' in desc1:
                return [desc1]
        return []

    def parse_image_urls(self, response):
        image_urls = response.css('.image-gallery-item img::attr("data-lazysrc")').extract()
        main_image_url = response.css('.zoom-image::attr("data-zoom-uri")').extract_first()
        if image_urls:
            return [re.sub('baur_format_.', 'formatz', url) for url in image_urls]
        else:
            return [main_image_url]

    def parse_skus(self, response):
        skus = {}
        product_variants = json.loads(response.text)
        for item in product_variants['variants']:
            axis_data = item['axisData']
            try:
                skus[item['sku']] = {
                    'colour': axis_data[0]['value'],
                    'size': axis_data[1]['value'],
                    'currency': response.meta['currency'],
                    'price': response.meta['price'],
                    'previous_price': response.meta['previous_price']
                }
            except IndexError:
                pass
        product = response.meta['product']
        product['skus'] = skus
        return product
